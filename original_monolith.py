def main():
    name = input("Enter student name: ")
    marks = []

    for i in range(3):
        mark = float(input(f"Enter marks for subject {i + 1}: "))

        while mark < 0 or mark > 100:
            print("Invalid marks. Enter 0-100.")
            mark = float(input(f"Enter marks for subject {i + 1}: "))

        marks.append(mark)

    total = sum(marks)
    average = total / len(marks)

    if average >= 80:
        grade = "A"
    elif average >= 70:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 50:
        grade = "D"
    else:
        grade = "F"

    print("\nStudent Result")
    print("----------------")
    print("Name:", name)
    print("Total:", total)
    print("Average:", average)
    print("Grade:", grade)

main()
