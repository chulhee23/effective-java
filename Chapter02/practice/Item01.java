package Chapter02.practice;

public class Item01 {
    public static void main(String[] args) {
        Laptop laptop = Laptop.ofModelNameAndCompany("macbook Pro 16", "Apple");
        System.out.println("laptop = " + laptop);
    }
}
