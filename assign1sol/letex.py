# <Rayne Allen>
#

# CS358 Fall'24 Assignment 1 (Part B)
#
# LetEx - an expression language with let binding

from lark import Lark, v_args
from lark.visitors import Interpreter

# 1. Grammar
#
grammar = """

    ?expr0: "let" ID "=" expr0 "in" expr0 -> letop
        | expr

    ?expr: expr "+" term -> add
        | expr "-" term -> sub
        | term

    ?term: term "*" atom -> mul
        | term "/" atom -> div
        | atom

    ?atom: "(" expr0 ")" -> parens
        | ID -> var
        | NUM -> num 


    %import common.CNAME -> ID
    %import common.NUMBER -> NUM
    %import common.WS_INLINE
    %ignore WS_INLINE

"""

# Parser
#
# E.g. let x=1 in x+1
#      => let
#           x
#           num   1
#           add
#             var x
#             num 1
#
parser = Lark(grammar, start='expr0')


# 2. Variable environment
#
class Env(dict):
    def extend(self,x,v):
        #extend the environment by adding a new binding for variable x with value v
        if x in self:
            self[x].insert(0,v) #push new value onto the stack for variable x

        else:
            self[x] = [v] #create a new stack for variable x with value v

    def lookup(self,x): 
        #lookup the value of variable x
        val = super().get(x)

        if not val:
            raise Exception(f"Variable {x} not found") #raise an exception if variable x is not found
        
        return val[0] #return the top value of the stack for variable x

    def retract(self,x):
        # remove the most recent binding for variable x
        assert x in self, f"Variable {x} not found" + x
        self[x].pop(0) #pop the top value off the stack for variable x
        if not self[x]:
            del self[x] #delete the stack for variable x if it is empty

env = Env()

# 3. Interpreter
#
# E.g. (for the above example)
#      => 2
#
@v_args(inline=True)
class Eval(Interpreter):

    #interpret the let expression: let x = exp in body

    def letop(self, x, exp, body):
        val = self.visit(exp) #evaluate the expression assigned to the variable x
        env.extend(x, val) #extend the environment by adding a new binding for variable x with value val
        result = self.visit(body) #evaluate the body of the let expression
        env.retract(x) #remove the most recent binding for variable x
        return result #return the result of evaluating the body of the let expression
    
    def var(self, x):
        return env.lookup(x) #lookup the value of variable x
    
    def num(self, n):
        return int(n) #return the integer value of n
    
    def add(self, left, right):
        return self.visit(left) + self.visit(right) #add the values of left and right
    
    def sub(self, left, right):
        return self.visit(left) - self.visit(right) #subtract the value of right from left
    
    def mul(self, left, right):
        return self.visit(left) * self.visit(right) #multiply the values of left and right
    
    def div(self, left, right):
        return self.visit(left) / self.visit(right) #divide the value of left by right
    
    def parens(self, expr):
        return self.visit(expr) #evaluate the expression in parentheses


def main():
    while True:
        try:
            expr = input("Enter a let expr: ")
            tree = parser.parse(expr)
            print(expr)
            print(tree.pretty(), end="")
            print("tree.Eval() =", Eval().visit(tree))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == '__main__':
    main()
