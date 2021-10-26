# 아이템 06. 불필요한 객체 생성을 피하라

- 객체 재사용? 웬만해선 좋다!
- 다음 경우는 하지마!

### 같은 값임에도 다른 레퍼런스

```java
// bad case
String s = new String("asdf");

// good 
String s = "asdf";
  
// logg 사용 시 bad
log.info("INFO : "  + post); // 매번 String 객체 할당된다.
// good
log.info("INFO : {}", post);

// Boolean 비교 시 bad
Boolean(String) // 생성자로 쓰지 말고,
// good
Boolean.valueOf(String); // 처럼 팩터리 메서드를 사용해라
```



### 재사용 빈도가 높고 생성 비용이 비싼 경우

생성 비용이 비싸다면 **캐싱을 고려해라!**

자주 쓰는 값이라면 static final 로 초기에 캐싱해두고 재사용하자.

```java
static boolean isRomanNumeral(String s) {
  return s.matches("~~~~~");
}
```

- **문제점**
  - String.matches 는 문자열 형태를 확인하는 가장 쉬운 방법이지만,
    성능이 중요할 땐 반복해서 쓰기 적합하지 않음
- **개선**
  - 정규표현식을 표현하는 Pattern 인스턴스를 클래스 정적 초기화 과정에서 직접 생성해두고, 이 인스턴스를 재사용하자.

```java
public class RomanNumerals {
  private static final Pattern ROMAN = Pattern.compile("~~~");
  
  static boolean isRomanNumeral(String s) {
    return ROMAN.matcher(s).matches();
  }
}
```

이렇게 필드르 캐싱해두면 좋은데 지연 초기화는 잘 고려해서 쓰자.

지연 초기화하면 처음 호출될 때 초기화하니까 장점은 있지만, 코드의 복잡도가 더 올라갈 수도...



### 같은 인스턴스를 대변하는 여러 개의 인스턴스를 생성하지 말자

예) 

Map 인터페이스의 KeySet 메서드는 Map 객체 안의 키 전부를 담은 뷰를 반환.
KeySet 호출할 때마다 새로운 Set 인스턴스를 반환할 필요가 전혀 없다!





### 오토 박싱

: 기본 타입과 박싱된 기본 타입을 섞어 쓸 때 자동으로 상호 변환해주는 기술.

**오토박싱은 기본 타입과 그에 대응하는 박싱된 기본 타입의 구분을 흐려주지만, 완전히 없애주지는 않는다.**

>  Boxing 타입보다는 원시 타입을 권장

예를 보는게 가장 나을듯!

```java
private long sum() {
  Long sum = 0L;
  for(long i = 0; i < Integer.MAX_VALUE; i++){
    sum += i;
  }
  return sum;
}
```

`Long` 과 `long` 사이에서 오토박싱이 계속 이뤄진다.



**즉, 박싱 타입을 남용하지 않도록 주의하면서, 오토 박싱을 조심하자!**



### Util Class 에서도 원시타입(Primitive Type)을 권장한다

참, 거짓을 response 하는데 박싱 타입을 사용하는 것은 낭비다!

```java
public class PhonePatternUtil {
  private final String pattern;
  public boolean isValid(String phone){
    // ....
  }
}
```

- isValid 가 null 이 나올 경우가 있을까? 굳이 박싱 타입 쓰지 말고 원시 타입 쓰자!



### 그렇다면, 항상 원시타입이 옳은가?

대표적인 null case 를 보자

- `int price;`
- `Integer price;`
- price 가 0 인 것과 null 은 의미가 완전히 다르다!
  - null 은 가격이 아직 미정!



### 주의해야 할 내장 Method

그래서 위에서 봤던 matches 주의해야 하는 이유 자세히 보자!

```java
static boolean isEmailValid(String s) {
  return s.matches("~~~~~");
}

// String.java
public boolean matches(String expr) {
   return Pattern.matches(expr, this);
}

// Pattern.java
public static boolean matches(String regex, CharSequence input) {
  Pattern p = Pattern.compile(regex);
  Matcher m = p.matcher(input);
  return m.matches();
}
```

**내부적으로 객체가 계속 만들어지고 있었던 상황!!**



#### 최적화해보자!

- Pattern Instance가 한 번만 생성되도록

```java
public class EmailUtil {
  private static final Pattern EMAIL = Pattern.compile("~~~~");
  
  static boolean isEmailValid(String s) {
    return EMAIL.matcher(s).matches();
    // 객체의 생성을 없앴다!
  }
}
```



## 정리

- 무심결에 객체를 과도하게 생성했는지 점검
- 원시 타입과 박싱 타입 의미 정확하게 구분해서 사용하고 있는가?!
