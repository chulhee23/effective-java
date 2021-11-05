# 아이템 10. equals 는 일반 규약을 지켜 재정의 하라



equals 메서드는 재정의하기 쉬워보이지만, 잘못하면 최악의 결과가...

다음 상황에 해당하면 재정의하지말자.

- 각 인스턴스는 본질적으로 고유하다
  - Thread 가 좋은 예시!
- 인스턴스의 논리적 동치성을 검사할 일이 없다
- **상위 클래스에서 재정의한 Equals 가 하위 클래스에도 들어맞는다**
  - 대부분의 Set 구현체는 AbstractSet이 구현한 equals 를 상속받아 쓰고, List 는 Abstractlist를 상속받아 그대로 쓴다. (Map 도 마찬가지)
- 클래스가 private 이거나 package-private 이고, equals 메서드를 호출할 일이 없다
  - 만일 쓰는걸 원천봉쇄하려면 equals 를 오버라이드해서 throw Exception 하자



## 그럼 언제 재정의해야 하는가?

객체 식별성(물리적으로 동일한가)이 아니라 
**논리적 동치성을 확인해야할 때!**

equals 를 재정의할 때는 반드시 일반 규약을 따라야 한다.

### **반사성**

- x.equals(x) == true

```java
public class Fruit{
  private String name;

  public Fruit(String name){
    this.name = name;
  }

  public static void main(){
    List<Fruit> list = new ArrayList<>();
    Fruit f = new Fruit("apple");
    list.add(f);
    list.contains(f); // false일 경우에는 반사성을 만족하지 못하는 경우이다.
  }
}
```



### 대칭성

- x.equals(y) true 이면 y.equals(x) 도 true
- 두 객체는 서로에 대한 동치 여부에 똑같이 답해야 한다.

```java
// 대칭성을 위반한 클래스
public final class CaseInsensitiveString{
  private final String s;

  public CaseInsensitiveString(String s){
    this.s = Obejcts.requireNonNull(s);
  }

  @Override public boolean equals(Object o){
    if(o instanceof CaseInsensitiveString)
      return s.equalsIgnoreCase(((CaseInsensitiveString) o).s);
    if(o instanceof String) // 한방향으로만 작동한다.
      return s.equalsIgnoreCase((String) o);
    return false;
  }
}
```

```java
CaseInsensitiveString cis = new CaseInsensitiveString("Polish");
String s = "polish";

cis.equals(s); // true
s.equals(cis); // false
```

```java
//대칭성을 만족하게 수정
@Override public boolean equals(Object o){
  return o instanceof CaseInsensitiveString && ((CaseInsensitiveString) o).s.equalsIgnoreCase(s); // String에 대한 instanceof 부분을 빼고 구현한다.
}
```

### 추이성

- x -> y , y -> z 이면 x -> z 도 true
  - 이 조건 때문에 equals를 재 정의 하면 안되는 경우에 superclass에서 equals를 정의한 경우를 언급함

Point를 확장한 ColorPoint 라는 클래스를 가정해보자.

#### 잘못된 코드 1 - 대칭성 위배

```java
@Override public boolean equals(Obejct o){
  if(!(o instanceof Point))
    return false;
  if(!(o instanceof ColorPoint))
    return o.equals(this);
  return super.equals(o) && ((ColorPoint) o).color == color;
}
```

Point 의 equals 는 색상을 무시하고, ColorPoint의 equals 는 입력 매개변수의 클래스 종류가 다르다면 매번 false 만 반환.

```java
Point p = new Point(1,2);
ColorPoint cp = new ColorPoint(1,2, Color.RED);
p.equals(cp);    // true (Point의 equals로 계산)
cp.equals(p);    // false (ColorPoint의 equals로 계산: color 필드 부분에서 false)
```

#### 잘못된 코드 2 - 추이성 위배

이번엔 색상을 무시하도록 해결하고자 했다.

```java
@Override public boolean equals(Obejct o){
  if(!(o instanceof Point))
    return false;
  // o가 일반 Point 면 색상 무시하교 비교
  if(!(o instanceof ColorPoint))
    return o.equals(this);

  // o가 ColorPoint면 색상까지 비교
  return super.equals(o) && ((ColorPoint) o).color == color;
}

```

```java
ColorPoint p1 = new ColorPoint(1,2, Color.RED);
Point p2 = new Point(1,2);
ColorPoint p3 = new ColorPoint(1,2, Color.BLUE);
p1.equals(p2);    // true (ColorPoint의 equals 비교 //2번째 if문에서 Point의 equals로 변환)
p2.equals(p3);    // true (Point의 equals 비교 // x,y 같으니 true)
p1.equals(p3);    // false (ColorPoint의 equals 비교)
```

구체 클래스를 확장해 새로운 값을 추가하면서 equals 규약을 만족시킬 방법은 존재하지 않는다.

**그렇다고 instanceof 검사 대신 getClass 검사를 하라는 것은 아니다.**
리스코프 치환 원칙에 위배되니깐!

#### 상속대신 컴포지션을 사용해라!

```java
public class ColorPoint{
  private final Point point;
  private final Color color;

  public Point asPoint(){ //view 메서드 패턴
    return point
  }

  @Override public boolean equals(Object o){
    if(!(o instanceof ColorPoint)){
      return false;
    }
    ColorPoint cp = (ColorPoint) o;
    return cp.point.equals(point) && cp.color.equals(color);
  }
}
```



#### 추상클래스의 하위 클래스 사용하기

추상클래스의 하위클래스에서는 equals 규약을 지키면서도 값을 추가할 수 있다.
상위 클래스를 직접 인스턴스로 만드는게 불가능하기 때문에 하위클래스끼리의 비교가 가능해지기 때문인 것 같다.



### 일관성

- 항상 x.equals(y) true

가변 객체 = 비교 시점에 따라 서로 다를 수 있다.
불변 객체 = 한번 다르면 끝까지 달라야 한다.

equals는 항시 메모리에 존재하는 객체만을 사용한 결정적(deterministic) 계산만 수행해야 한다.

**클래스가 불변이든 가변이든 equals의 판단에 신뢰할 수 없는 자원이 끼어들면 안된다 : ex URL과 매핑된 호스트의 IP 주소**

 

### null 아님

- null 이 아닌 모든 참조값 x 에 대해 x.equals(null) 은 false

**명시적 null 검사**

```java
@Override public boolean equals(Object o){
  if( o == null){
    return false;
  }
}
```

**묵시적 null 검사**

```java
@Override public boolean equals(Obejct o){
  if(!(o instanceof MyType)) // instanceof 자체가 타입과 무관하게 null이면 false 반환함.
    return false;
  MyType mt = (MyType) o;
}
```



## 양질의 equals 메서드 구현 방법

### 1. == 연산자를 사용해 입력이 자기 자신의 참조인지 확인한다.

단순한 성능 최적화용! 비교 작업이 복잡할 때 제역할 할 것.

### 2. instanceof 연산자로 입력이 올바른 타입인지 확인한다.

- 올바른 타입의 경우 
  - equals 가 정의된 클래스로 리턴되는가?
- 올바르지 않은 타입의 경우( equals 을 구현한 인터페이스)
  - 서로 다른 클래스 간 비교가 가능하게 해야한다.
  - 인터페이스의 equals 를 비교해야한다!

### 3. 입력을 올바른 타입으로 형변환 한다.

형변환은 무조건 성공. 2번에서 이미 검사했기 때문!

### 4. 입력 객체와 자기 자신의 대응되는 '핵심' 필드들이 모두 일치하는지 하나씩 검사한다.

2번에서 인터페이스를 사용했다면 입력의 필드값을 가져올 때도 인터페이스 메서드를 사용해야한다.



## Equals 구현 시 추가 주의사항

- **기본타입** : == 연산자 비교

- **참조타입** : equals() 비교

- **float, double 필드** : Float.compare(float, float), Double.compare(double, double) 비교 (부동 소수 값)
  - Float.equals(float)나 Double.equals(double) 은 **오토 박싱**을 수반할 수 있어 성능상 좋지 않다.

- **배열 필드** : 원소 각각을 지침대로 비교한다. / 모두가 핵심 필드라면 Arrays.equals()를 사용한다.

 

- Object.equals(object, object) 로 비교하여 NullPointException 발생을 예방

- 필드의 표준형을 저장해 둔 뒤 표준형끼리 비교하자(불변 클래스(아이템 17)에 제격)

  - 가변 객체라면 값이 바뀔 때마다 표준형을 최신상태로 갱신해줘야함

- equals 재정의 시 hashCode 도 반드시 재정의 하 (아이템 11)

- 너무 복잡하게 해결하려들지 말자

  - 동치성만 검사해도 규약을 지킬 수 있다. 

- Object 외 타입으로 받는 equals 는 선언하지 말자!

  - ```java
    public boolean equals(MyClass o) // @Override가 아니다! 
    // 오버로딩...
    ```



AutoValue 프레임워크도 있다.

https://www.baeldung.com/introduction-to-autovalue



## 핵심 정리

꼭 필요한 경우가 아니라면 equals 재정의하지 말자. 재정의해야한다면, 그 클래스의 핵심 필드를 모두 빠짐없이 5가지 규약 지켜가면서 비교해야 한다.

### 전형적인 검사 패턴

1. == 를 통해 input 이 자기 자신 참조인지
2. instanceof 를 통해 타입이 명확한지
3. 2를 통해 올바른 타입으로 형 변환
4. 핵심 필드들이 모두 일치하는지
5. not null 

ㅌ