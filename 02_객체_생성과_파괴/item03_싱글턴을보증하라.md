# private 생성자나 열거 타입으로 싱글턴임을 보증하라

- 싱글턴 : 인스턴스를 오직 하나만 생성할 수 있는 클래스
  - **무상태 객체**나 설계상 유일해야하는 시스템 컴포넌트
  - 클래스를 싱글턴으로 만들면 이를 사용하는 클라이언트를 테스트하기 어렵다.
  - 타입을 인터페이스로 정의한 다음, 그 인터페이스 구현해서 만든 싱글턴이 아니라면
    싱글턴 인스턴스를 가짜(mock) 구현으로 불가

- **싱글턴 만들기**
  - 생성자 private + 인스턴스 접근 메서드 public static 으로 선언
    - 정적 팩토리 메서드를 **public static 멤버**로 제공
  -  Enum 으로 생성
    - 근데 비추천.... 팀에서 합의를 하거나...!

```java
public class Speaker {
  private static final Speaker INSTANCE = new Speaker();
  private Speaker() {}
  public static Speaker getInstance() {return INSTANCE;}
}
```



상황에 따라 synchronized 나, lazy 하게 인스턴스 생성할 수도 있다.

```java
public class Speaker {
  private static Speaker instance;
  private Speaker() {}
  
  public static synchronized Speaker getInstance() {
    if (instance == null) {
      instance = new Speaker();
    }
    return instance;
  }
}
```

이렇게 한다면 비용을 조금 아낄 수 있겠다!

- 커넥션을 싱글톤으로 /  연결 되어있다가 끊기면 새롭게 생성할 수 있겠다!



