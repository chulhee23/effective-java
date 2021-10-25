package Chapter02.practice;

public class Laptop {
    private String modelName;
    private String company;

    public String getModelName() {
        return modelName;
    }

    public void setModelName(String modelName) {
        this.modelName = modelName;
    }

    public String getCompany() {
        return company;
    }

    public void setCompany(String company) {
        this.company = company;
    }

    public static Laptop ofModelNameAndCompany(String model, String company){
        Laptop laptop = new Laptop();
        laptop.company = company;
        laptop.modelName = model;
        return laptop;
    }


}

