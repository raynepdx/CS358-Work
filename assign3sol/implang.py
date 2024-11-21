# <Rayne Allen, PSU ID: 963230784>
#

# CS358 Fall'24 Assignment 3 (Part A)
#
# ImpLang - a simple imperative language with nested scopes

# ImpLang - an imperative language
#
#   prog -> stmt
#
#   stmt -> "var" ID "=" expr
#         | ID "=" expr 
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

grammar = """
  ?start: stmt

   stmt: "var" ID "=" expr         -> decl
       | ID "=" expr               -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> ifstmt
       | "while" "(" expr ")" stmt -> whstmt
       | "print" "(" expr ")"      -> prstmt
       | "{" stmt (";" stmt)* "}"  -> block      

  ?expr: expr "+" term  -> add
       | expr "-" term  -> sub
       | term         

  ?term: term "*" atom  -> mul
       | term "/" atom  -> div
       | atom

  ?atom: "(" expr ")"
       | ID             -> var
       | NUM            -> num

  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

# With an 'lalr' parser, Lark handles the 'dangling else' 
# case correctly.
parser = Lark(grammar, parser='lalr')

debug = False

# Variable environment
#
class Env(dict):
    def __init__(self): #stack to keep track of scopes
        self.prev_envs = []

    def open_scope(self): #open a new scope
        self.prev_envs.append(self.copy()) 
        return Env()
    
    def close_scope(self): #close the current scope, go back to the previous scope
        if not self.prev_envs:
            raise Exception("No enclosing scope")
        return self.prev_envs.pop()
    
    def extend(self, var, val): #add a new variable to the current scope
        if var in self:
            raise Exception(f"Variable {var} already declared")
        self[var] = val

    def lookup(self, var):
        if var in self:
            return self[var]
        for scope in reversed(self.prev_envs):
            if var in scope:
                return scope[var]
        raise Exception(f"Variable {var} not declared")
    

    def update(self, var, val): #update the value of a variable in the current scope
        if var in self:
            self[var] = val
            return
        for scope in reversed(self.prev_envs):
            if var in scope:
                scope[var] = val
                return
        raise Exception(f"Variable {var} not declared")
    
    def display(self, output="Current environment:"): #display the current scope and previous scopes. I'm adding the latter for debugging purposes
        print(output)
        print("Current scope:", self)
        print("Previous scopes:", self.prev_envs)


    

env = Env()

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self):
        self.env = Env() #not sure if this is necessary since num was the first given function, but i like to add a constructor to my classes

    def num(self, val): 
        return int(val)
    
    def var(self, var): #find the value of the var in the current scope
        return self.env.lookup(var)
    
    def declare(self, var, val): #declare a new variable in the current scope
        val = self.visit(val)
        self.extend(var, val)

    def assign(self, var, val): #assign a new value to a variable in the current scope
        val = self.visit(val)
        self.env.assign(var, val)

    def add(self, x, y): #add two values
        return self.visit(x) + self.visit(y)
    
    def sub(self, x, y): #subtract two values
        return self.visit(x) - self.visit(y)
    
    def mul(self, x, y): #multiply two values
        return self.visit(x) * self.visit(y)
    
    def div(self, x, y): #divide two values
        return self.visit(x) / self.visit(y)
    
    def print_statement(self, val): #print a value
        print(self.visit(val))

    def if_statement(self, cond, stmt1, stmt2): #if statement
        if self.visit(cond):
            self.visit(stmt1)
        else:
            self.visit(stmt2)

    def while_statement(self, cond, stmt): #while loop
        while self.visit(cond):
            self.visit(stmt)

    def block(self, *stmts): #open a new scope for the block
        self.env = self.env.open_scope()
        try:
            for stmt in stmts:
                self.visit(stmt)

        finally:
            self.env = self.env.close_scope()

    




    

# A new input routine - sys.stdin.read() 
# - It allows source program be written in multiple lines
#
import sys
def main():
    try:
        prog = sys.stdin.read()
        tree = parser.parse(prog)
        print(prog)
        Eval().visit(tree)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

