import os

index = ["", "", "2장 객체 생성과 파괴",
 "3장 모든 객체의 공통 메서드",
 "4장 클래스와 인터페이스",
 "5장 제네릭",
 "6장 열거 타입과 애너테이션",
 "7장 람다와 스트림",
 "8장 메서드",
 "9장 일반적인 프로그래밍 원칙",
 "10장 예외",
 "11장 동시성",
 "12장 직렬화"]

with open('README.md', 'w') as outfile:
    table_of_contents = []

    # merge readme
    for files in os.listdir("./"):
        if os.path.isdir(files):
            pwd = files
            for ff in sorted(os.listdir(pwd)):
                readme = pwd + "/" + ff
                if ".md" in ff:
                    with open(readme) as infile:
                        first_line = infile.readline().rstrip()
                        table_of_contents.append([first_line, readme])

    # 목차 생성
    outfile.seek(0)
    outfile.write("# Effective Java \n\n")

    current_chapter_num = 1
    for readme_head, pwd in table_of_contents:
        chapter_number = int(pwd[7:9])

        if current_chapter_num < chapter_number:
            current_chapter_num = chapter_number
            
            outfile.write(f"\n## {index[current_chapter_num]} \n")
        
        head = readme_head[2:]
        outfile.write(f"- [{head}]({pwd})\n")

    outfile.write("\n\n")

index = ["", "", "2장 객체 생성과 파괴",
         "3장 모든 객체의 공통 메서드",
         "4장 클래스와 인터페이스",
         "5장 제네릭",
         "6장 열거 타입과 애너테이션",
         "7장 람다와 스트림",
         "8장 메서드",
         "9장 일반적인 프로그래밍 원칙",
         "10장 예외",
         "11장 동시성",
         "12장 직렬화"]

with open('README.md', 'w') as outfile:
    table_of_contents = []

    # merge readme
    for files in os.listdir("./"):
        if os.path.isdir(files):
            pwd = files
            for ff in sorted(os.listdir(pwd)):
                readme = pwd + "/" + ff
                if ".md" in ff:
                    with open(readme) as infile:
                        first_line = infile.readline().rstrip()
                        table_of_contents.append([first_line, readme])

    print(table_of_contents)
    
    # 목차 생성
    outfile.seek(0)
    outfile.write("# Effective Java \n\n")

    current_chapter_num = 1
    for readme_head, pwd in table_of_contents:
        chapter_number = int(pwd[7:9])

        if current_chapter_num < chapter_number:
            current_chapter_num = chapter_number

            outfile.write(f"\n## {index[current_chapter_num]} \n")

        head = readme_head[2:]
        outfile.write(f"- [{head}]({pwd})\n")

    outfile.write("\n\n")
