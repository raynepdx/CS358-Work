#Rayne Allen
#PSU ID: 963230784

# exercise 7.1a


class Lambda:
    pass

class Var(Lambda):
    def __init__(self, name):
        self.name = name #name of the variable


class Def(Lambda):
    def __init__(self, param, body):
        self.param = param #parameter name
        self.body = body #body of the function

class App(Lambda):
    def __init__(self, func, arg):
        self.func = func #function
        self.arg = arg #argument


# exercise 7.1b

l_expr = Def("x", Def("y", App(Var("x"), Var("y"))))
l_expr2 = App(Def("x", App(Var("x"), Var("x"))), Var("y"))



# exercise #7.2a
"""
1) When A's constructor is uncommented, the object of C calls A's constructor. This is because C is a child of A and doesnt override the constructor.
   A's constructor is called and x is set to 2. When the object of C is created, it prints 2.
2) With both constructors uncommented, C's constructor overrides A's, so when the object of C is created, it prints 'init C'.

"""

# exercise #7.2b
"""
I'd imagine that because there is diamond inheritance, the order of the program execution would be the constructors for C, B2, B1, and A, respectively. 
Typing this after compiling the program: okay, so I see that the order of execution is C, B1, B2, and A. I think this is because the parents of C are listed as B1 and B2, so B1 is called first, then B2, and finally A.
"""

# exercise #7.2c
"""
Okay, so if the order of execution is C, B1, B2, A, and C starts at 1, and  the object calls super().__init__(x+1), then the value of w is 1, y is 2, z is 3, and x is 4.
The program would essentially just climb through the hierarchy and increment 1 to each value per constructor call.
Typing after I compiled: Yep, I was right. I'm not 100% if it was for the right reason though. Either way, woohoo?
"""


# exercise #7.3a
class Overload:
    def aMethod(self, a=None, b=None):
        if a is not None and b is not None:
            print(f"a: {a}, b: {b}")
        elif a is not None:
            print(f"a: {a}")
        else:
            print("No arguments")

obj = Overload()
obj.aMethod()
obj.aMethod(1)
obj.aMethod(1, 2)



# exercise #7.3b
class Parent:
    def hello(self):
        print("Hello world")

class Child(Parent):
    def hello(self):
        print("World hello")


obj1 = Parent()
obj2 = Child()

obj1.hello()
obj2.hello()



# exercise #7.3c
"""
Python does not support method overloading like C++, where we can have multiple methods with the same name but different parameters. We can only define one method with a given name in a class, with
the last method defined being the one that is used. We can do overriding though! a child class can always redefine a method from its parent class, with Python knowing to use the correct method based on the object's type.
"""