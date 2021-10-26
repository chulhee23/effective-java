# 아이템 04. 인스턴스화를 막으려거든 private 생성자를 사용하라

정적 메서드 + 정적 필드만 있는 클래스가 만들고 싶을 수도 있음.
(물론 OOP 적으로 생각하지 않으면 남용하게 되는 방식...)

java.lang.Math, java.util.Arrays 처럼 모아놓을 수 있겠다.



- 이처럼 정적멤버만 담은 유틸리티 클래스는 **인스턴스 만들어 쓰려고 설계하지 않았다.**
- 그런데 컴파일러가 생성자 없으면 자동으로 기본 생성자 만든다.
  - -> 의도치 않은 인스턴스 생성 가능

### 추상클래스로 만들어서 해결할 수 있을까?

A ) 막을 수 없다.
하위 클래스로 만들어 인스턴스화 하면 끝!

**private 생성자로 만들어서 해결하자!**

```java
private 생성자() {
  throw new AssertionError();
}
```



- human error를 방지하기 위해 private 생성자를 권장한다!
  - Util 클래스처럼 관용적으로 인스턴스화 하지 않을거라고 모두 이미 알고 있는 경우는 생략하기도 하짐나....
    웬만해선 private 달아두자!
