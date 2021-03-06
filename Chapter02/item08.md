# 아이템 08. finalizer 와 cleaner 사용을 피하라



자바의 객체 소멸자

- finalizer
  - 예측할 수 없고, 상황에 따라 위험할 수도 있어 불필요
  - 기본적으로 **쓰지 말아야**
  - java 9 -> **deprecated**
- cleaner
  - finalizer 보다는 덜 위험하지만, 여전히 예측불가 + 느림 + 불필요



finalizer 와 cleaner 는 언제 실행되는지 알 수 없다(즉시 수행된다는 보장 X)

예 ) 파일 닫기를 finalizer 나 cleaner 에게 맡기면 오류 발생 가능
시스템이 동시에 열 수 있는 파일 개수 한계가 있어서 finalizer 나 cleaner가 실행을 느리게 하면 새로운 파일을 열지 못해 프로그램이 실패할 수 있음!





## 대안은?

AutoCloseable 을 구현해주고, 클라이언트에서 인스턴스를 다 쓰고 나면 close 메서드를 호출한다.

구체적인 구현법과 관련하여 각 인스턴스는 자신이 닫혔는지를 추적하는 것이 좋다.

즉, close 메서드에서 해당 객체가 더 이상 유효하지 않음을 필드에 기록, 다른 메서드는 이 필드를 검사해서 close 이후 호출되었다면 IllegalStateException 을 던지자.



### 그럼 finalizer 나 cleaner는 어디에 쓰는가?

- 자원의 소유자가 close 메서드를 호출하지 않는 것에 대비한 안전망 역할
- 네이티브 피어와 연결된 객체
  - 네이티브 피어 : 일반 자바 객체가 네이티브 메서드를 통해 기능을 위임한 네이티브 객체
  - 네이티브 피어는 자바 객체가 아니므로 GC가 그 존재를 모름
    - cleaner 나 finalizer 가 처리해야함!







## 정리

- 특수한 상황이 아니라면 사용하지말자!
- 안정망 역할로 아주 제한적인 사용만 가능

> 음... 와닿지 않는 아이템