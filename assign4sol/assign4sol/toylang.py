# <Rayne Allen>
#

# CS358 Fall'24 Assignment 4 (Part A)
#
# ToyLang - an imperative language with lambda functions
#
#   prog -> stmt
#
#   stmt -> "var" ID "=" expr
#         | "print" "(" expr ")"
#         | "{" stmt (";" stmt)* "}" 
#
#   expr -> "lambda" ID ":" expr
#         | expr "(" expr ")"
#         | aexpr 
#
#   aexpr -> aexpr "+" term
#          | aexpr "-" term
#          | term         
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

debug = False

grammar = """
  ?start: stmt

   stmt: "var" ID "=" expr         -> decl
       | "print" "(" expr ")"      -> prstmt
       | "{" stmt (";" stmt)* "}"  -> block    

  ?expr: "lambda" ID ":" expr      -> func
       | expr "(" expr ")"         -> call
       | aexpr 

  ?aexpr: aexpr "+" term  -> add
       |  aexpr "-" term  -> sub
       |  term         

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

parser = Lark(grammar, parser='lalr')

#env class to handle binding and scoping
class Env:
    def __init__(self, outer=None):
        #dict for current scope
        self.vars = {}
        #outer scope
        self.outer = outer

    #get a var's value
    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.outer:
            return self.outer.get(name)
        else:
            raise NameError(f"Undefined variable: {name}")


    #update var in current scope
    def set(self, name, value):
        self.vars[name] = value

env = Env()

# Closure
#
class Closure():
    def __init__(self,id,body,env):
        self.id = id
        self.body = body
        self.env = env

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self):
        self.env = Env()


    def num(self, val):  
        return int(val)


    #variable ID
    def var(self, name):
        return self.env.get(name)


    #variable declaration
    def decl(self, name, expr):
        value = self.visit(expr)
        self.env.set(name, value)


    
    def prstmt(self, expr):
        value = self.visit(expr)
        print(value)


    #handle stmt block
    def block(self, stmt, *stmts):
        outer = self.env
        self.env = Env(outer)
        try:
            self.visit(stmt)
            for s in stmts:
                self.visit(s)
        finally:
            self.env = outer


    #arithmetic ops
    def add(self, left, right):
        return self.visit(left) + self.visit(right)

    def sub(self, left, right):
        return self.visit(left) - self.visit(right)

    def mul(self, left, right):
        return self.visit(left) * self.visit(right)

    def div(self, left, right):
        return self.visit(left) // self.visit(right)


    #handle lambda exprs
    def func(self, param, body):
        return Closure(param, body, self.env)


    #handle function calls (expr(expr))
    def call(self, func_expr, arg_expr):
        closure = self.visit(func_expr)
        if not isinstance(closure, Closure):
            raise TypeError(f"{closure} is not a function")

        #eval arg expr
        arg = self.visit(arg_expr)

        #create new env for func execution
        new_env = Env(closure.env)
        new_env.set(closure.id, arg)

        outer = self.env
        self.env = new_env

        try:
            return self.visit(closure.body)
        finally:
            self.env = outer

    

import sys
def main():
    try:
       #check command line file name
        filename = sys.argv[1] if len(sys.argv) > 1 else None
        if filename:
            with open(filename) as f:
                prog = f.read()

        else:
            prog = sys.stdin.read()

        tree = parser.parse(prog)

        Eval().visit(tree)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

