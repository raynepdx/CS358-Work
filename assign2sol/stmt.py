# <Rayne Allen>
#

# CS358 Fall'24 Assignment 2 (Part B)
#
# Stmt - a language with simple statements
#
#   prog -> stmt
#
#   stmt -> ID "=" expr 
#         | "if" "(" expr ")" stmt ["else" stmt]
#         | "while" "(" expr ")" stmt
#         | "print" "(" expr ")"
#         | "{" stmt (";" stmt)* "}" 
#
#   expr -> expr "+" term
#         | expr "-" term
#         | term         
#
#   term -> term "*" atom
#         | term "/" atom
#         | atom
#
#   atom: "(" expr ")"
#         | ID
#         | NUM
#
from lark import Lark, v_args
from lark.visitors import Interpreter
import sys

# Grammar
#
grammar = """
  ?start: stmt*

  ?stmt: assign ";"
        | ifstmt
        | whilestmt
        | printstmt ";"
        | block

    assign: ID "=" expr -> assign

    ifstmt: "if" "(" expr ")" stmt ("else" stmt)? -> ifstmt
    whilestmt: "while" "(" expr ")" stmt -> whilestmt
    printstmt: "print" "(" expr ")" -> printstmt
    block: "{"stmt*"}" -> block

    ?expr: expr ("<" | "<=" | ">" | ">=" | "==" | "!=") arith_expr -> compare
            | arith_expr

    ?arith_expr: expr "+" term -> add
            | expr "-" term -> sub
            | term

    ?term: term "*" atom -> mul
            | term "/" atom -> div
            | atom

    ?atom: NUM -> num
            | ID -> var
            | "(" expr ")"

  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

parser = Lark(grammar)

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self):
        super().__init__()
        self.env = {} #environment to store variables

    def var(self, name):
        #retrieve variable value from environment
        return self.env.get(str(name), 0)
    
    def assign(self, name, value):
        #assign variable value to environment
        self.env[str(name)] = self.visit(value)
        return self.env[str(name)]
    
    def ifstmt(self, cond, stmt, elsestmt=None): #if statement
        if self.visit(cond):
            return self.visit(stmt)
        elif elsestmt:
            return self.visit(elsestmt)
        return None
    
    def whilestmt(self, cond, stmt): #while statement
        while self.visit(cond):
            self.visit(stmt)
        
    def printstmt(self, expr): #print statement
        result = self.visit(expr)
        print(result) #print result

    def block(self, *stmts): #block statement
        for stmt in stmts:
            self.visit(stmt)
      


    def num(self, val):  return int(val)
    def add(self, x, y): return Eval().visit(x) + Eval().visit(y)
    def sub(self, x, y): return Eval().visit(x) - Eval().visit(y)
    def mul(self, x, y): return Eval().visit(x) * Eval().visit(y)
    def div(self, x, y): return Eval().visit(x) // Eval().visit(y)

    

def main():
    try:
        #check if a file is provided
        if len(sys.argv) > 1:
            with open(sys.argv[1]) as f:
                prog = f.read()
        else:
            prog = input("Enter a program: ")
        tree = parser.parse(prog)
        print(prog)
        print(tree.pretty(), end="")
        print(Eval().visit(tree))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

