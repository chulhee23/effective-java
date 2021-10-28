# 아이템 09. try-finally 보다는 try-with-resources 를 사용하라



전통적으로 자원이 제대로 닫힘을 보장하는 수단은 try-finally 가 많았다!

```java
try {
  return br.readLine();
} finally {
  br.close();
}
```

그러나 자원이 2개 이상이 된다면 코드가 지저분해진다! Try 문이 중첩되면서... 

- 예외가 try, finally 블록 모두에서 발생 가능하며,
  close 가 실패할 수 있다.
- try 문 이후 Close메서드까지 실패하게 되며 두 번째 예외가 첫 번째 예외를 집어삼킨다.
  - -> 디버깅 어려워진다!



## try-with-resources 로 해결된다!

이 구조를 사용하려면 AutoCloseable 인터페이스를 구현해야한다.

- AutoCloseable 인터페이스

  : 단순히 void 반환하는 close 메서드 하나만 정의된 인터페이스



- 변경전

- ```java
  BufferedReader br = new BufferedReader(new FileReader(path));
  try {
    return br.readLine();
  } finally {
    br.close();
  }
  ```

- 변경 후

- ```java
  try (BufferReader br = new BufferReader(new FileReader(path))){
    return br.readLine();
  }
  ```



정말 장점이 되었는지 확인해보자.

- readLine 과 close 호출 양쪽에서 예외가 발생한다면,
- Close 발생한 예외는 숨겨지고, readLine 에서 발생한 예외가 기록된다.
  - 프로그래머에게 보여줄 예외 하나만 보존되고 다른 예외가 숨겨질 수 있다.
- catch절 덕분에 try 문 중첩하지 않고 다수의 예외 처리 가능하다.





> Finally 가 필요하다면, try-with-resources 를 활용하자!!