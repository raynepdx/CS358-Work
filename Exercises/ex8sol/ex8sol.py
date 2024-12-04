#Rayne Allen
#ID: 963230784

# exercise 8.1a
#type error is adding an int and a string
x= 2 + "hello"

# exercise 8.1b
#type error for passing the wrong argument type to a function
def hello(name: str) -> str:
    return f"Hello, {name}"


# exercise 8.1c
#type error for assigning the wrong type to a variable with type annotation
age: int = "twenty"


# exercise 8.1d
#type error for accessing a non-existent field of a class
class Person:
    def __init__(self, name: str):
        self.name = name

p = Person("Rayne")
age = p.age #age is not a field of the Person class


#exercise 8.2
#runtime errorss not caught by mypy
#1) division by zero
x = 1/0

#2) accessing an index that is out of range
list = [1, 2, 3]
print(list[3])


