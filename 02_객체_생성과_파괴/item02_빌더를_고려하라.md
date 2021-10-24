# 아이템 2.  생성자에 매개변수가 많다면 빌더를 고려하라

객체를 생성할 때 매개변수가 많다면 크게 2가지 방식을 고려한다.

- 점층적 생성자 패턴
  - 여러개의 constructor 를 두게 된다
    - 클라이언트가 코드를 작성하기도 어렵고, 읽기도 어렵다.
    - 런타임에 버그 가능성 생긴다!
- Java beans Pattern (Setter)
  - 코드가 길어지긴 했지만, 인스턴스 만들기 쉽고, 읽기도 쉬움!
  - 객체 하나를 만들려면 여러 개의 메서드를 호출하고, 완전히 객체가 생성되기 전까지 일관성을 잃는다.
  - freeze 해서 얼리기 전에 사용 못하게 막기도 하지만 실전에서 거의 X

그러니 빌더를 쓰자!

```java
public class NutritionFacts {
  private final int servingSize;
  private final int servings;
  private final int calories;
  // ...
  
  public static class Builder {
    // 필수 매개변수
    private final int servingSize;
    private final int servings;
    
    // 선택 매개변수
    private final int calories = 0;
    // ...
    
    public Builder(int servingSize, int servings) {
      this.servingSize = servingSize;
      this.servings = servings;
    }
    
    // Build 과정에선 Builder 로 계속 리턴해서 chaining 을 의도하자
    public Builder calories(int val) {
      calories = val; 
      return this;
    }
    
    // ...
    public NutritionFacts build() {
      return new NutiritionFacts(this);
    }
  }
  
  private NutritionFacts(Builder builder){
    servingSize = builder.servingSize;
    // ...
  }
  
}
```

`NutritionFacts coke = new NutritionFacts.Builder(240, 8).calories(100).sodium(12).build();`

으로 사용 가능!

### Lombok 으로 쓰면?

lombok을 쓰면 더 간단하다.

```java
@Data
@Builder
public class NutritionFacts {
  private final int servingSize;
  private final int servings;
  @Builder.Default private final int calories = 0;
  @Builder.Default private final int sodium = 0;
  // ...
  
}
```

```java
// Build
NutritionFacts coke = NutritionFacts.builder().servingSize(10).servings(50).sodium(10).build();
```



### Builder 의 장단점

- 장점
  - 상속받은 클래스의 빌더가 정의한 build 메서드가 상위 메서드의 타입을 return 하는 것이 아닌 자신의 타입을 return
- 단점
  - Builder 를 항상 만들어야 하기 때문에 생성비용 무조건 발생
  - 3~4개 이하의 파라미터에선 빌더가 더 안좋다.

