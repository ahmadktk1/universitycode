# Base Class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# Derived class Student
class Student(Person):
    def __init__(self, name, age, grade):
        super().__init__(name, age)
        self.grade = grade

    def display_info(self):
        print("Student Details:")
        print("Name:", self.name)
        print("Age:", self.age)
        print("Grade:", self.grade)
        print("--------------------")


# Derived class  Teacher
class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def display_info(self):
        print("Teacher Details:")
        print("Name:", self.name)
        print("Age:", self.age)
        print("Subject:", self.subject)
        print("--------------------")


# Creating objects
student1 = Student("Ali", 20, "A")
teacher1 = Teacher("Ammad", 35, "Mathematics")

# Calling methods
student1.display_info()
teacher1.display_info()
