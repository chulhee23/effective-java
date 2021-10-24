package Chapter02.practice;


public class LaptopDto {
    private String modelName;
    private String company;

    // Entity 보다는 DTO 로 전달
    public static LaptopDto from(Laptop laptop) {
        LaptopDto laptopDto = new LaptopDto();
        laptopDto.company = laptop.getCompany();
        laptopDto.modelName = laptop.getModelName();
        return laptopDto;
    }


}