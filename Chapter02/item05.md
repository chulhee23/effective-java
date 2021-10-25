# 아이템 05. 자원을 직접 명시하지 말고 의존 객체 주입을 사용하라



잘못된 예제를 일단 보고 가자.

```java
// 정적 유틸리티 잘못 사용
public class SpellChecker {
  private static final Lexicon dictionary = ...;
  private SpellChecker() {} // 객체 생성 방지
  
  public static boolean isValid(String word) {...}

}

```

- 위 코드는 유연하지도 않고, 테스트하기 어렵다.
  - dictionary 하나만 사용한다고 가정하면서 
    언어별, 특수 언어 처리, 테스트용 사전 구분이 모두 불가...!

외부에서 객체를 주입해서 유연하게 만들자!

```java
public class SpellChecker {
  private static final Lexicon dictionary;
  public SpellChecker(Lexicon dictionary) {
    this.dictionary = Object.requireNonNull(dictionary);
  } 
  
  public static boolean isValid(String word) {...}

}

```



### 의존성 주입 패턴의 변형 - 생성자에 자원 팩터리를 넘겨주는 방식

팩터리 : 호출할 때마다 특정 타입의 인스턴스를 반복해서 만들어주는 객체

예 ) `Supplier<T>` 인터페이스



### @Configuration

**Config class 내부에 직접 정의는 멈춰야한다!**

```java
@Configuration
public class AppConfig {
  private static final String address = "asd";
  // ...
}
```

여러 환경에서 다른 값들이 들어가야할 때 적절하지 않으며,
**내부에서 분기처리 하는 것 또한 좋지 않음!**



### Property Injection 으로 하자

```yml
# application.yml
config:
	address: "asdfasdf"
```

```java
@Configuration
public class AppConfig {
  @Value("${config.address}")
  private String address;
}
```

어플리케이션 실행할 때 application.yml 을 읽어와서 실행!



그렇다면, 위에서 특정 패턴에 대해서 검증하는 클래스의 유연성을 높여보자!

예 ) 국제 번호, 국내 번호 등 전화번호 검증 클래스에 대해서

```java
public class PhonePatternChecker {
  private final String pattern;
  
  public PhonePatternChecker(String pattern) {
    this.pattern = pattern;
  }
  public boolean isValid(String number) {
    //...
  }
  
}
```



### 정리

- ConfigClass 에서도 유연성 보장하고 있었는지
- 정말 싱글톤이어야 하는지(제대로 이해하고 쓰고 있는지!)
- DI 를 제대로 하는지!
  - 다형성을 보장하면서 ~~

