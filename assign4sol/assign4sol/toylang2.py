import sys
from lark import Lark, v_args
from lark.visitors import Interpreter

grammar = """
    ?start: stmt

   stmt: "var" ID "=" expr                -> decl
       | "def" ID "(" ID ")" "=" body     -> func_decl
       | ID "=" expr                      -> assign
       | "if" "(" expr ")" stmt ["else" stmt] -> if_stmt
       | "while" "(" expr ")" stmt        -> while_stmt
       | "print" "(" expr ")"             -> prstmt
       | "{" stmt (";" stmt)* "}"         -> block    

   body: "{" (stmt ";")* "return" expr "}" -> func_body

  ?expr: "lambda" ID ":" expr             -> func
       | expr "(" expr ")"                -> call
       | aexpr 

  ?aexpr: aexpr "+" term                  -> add
        | aexpr "-" term                  -> sub
        | term         

  ?term: term "*" atom                    -> mul
        | term "/" atom                   -> div
        | atom

  ?atom: "(" expr ")"
       | ID                               -> var
       | NUM                              -> num

  %import common.WORD   -> ID
  %import common.INT    -> NUM
  %import common.WS
  %ignore WS
"""

parser = Lark(grammar, parser='lalr')

#env class for scoping
class Env:
    def __init__(self, outer=None):
        self.vars = {}
        self.outer = outer

    #find the variable in the current scope
    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.outer:
            return self.outer.get(name)
        else:
            raise NameError(f"NameError: name '{name}' is not defined")
        
    #update current var's scope
    def set(self, name, value):
        self.vars[name] = value


#closure class
class Closure():
    def __init__(self, id, body, env):
        self.id = id
        self.body = body
        self.env = env



#interpreter class
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self):
        self.env = Env()

    #handle numbers
    def num(self, val):
        return int(val)
    
    #handle variables
    def var(self, name):
        return self.env.get(name)
    
    #handle var declarations
    def decl(self, name, expr):
        value = self.visit(expr)
        self.env.set(name, value)

    #handle variable assignments
    def assign(self, name, expr):
        value = self.visit(expr)
        if name not in self.env.vars:
            raise NameError(f"NameError: name '{name}' is not defined")
        self.env.set(name, value)


    #handle print statements
    def prstmt(self, expr):
        value = self.visit(expr)
        print(value)


    #block statements
    def block(self, stmt, *stmts):
        outer = self.env
        self.env = Env(outer)
        try:
            self.visit(stmt)
            for s in stmts:
                self.visit(s)

        finally:
            self.env = outer


    #if statements
    def if_stmt(self, cond, then_stmt, else_stmt=None):
        if self.visit(cond):
            self.visit(then_stmt)
        elif else_stmt:
            self.visit(else_stmt)

    #while loops
    def while_stmt(self, cond, stmt):
        while self.visit(cond):
            self.visit(stmt)


    #function declarations
    def func_decl(self, name, param, body):
        closure = Closure(name, body, self.env)
        self.env.set(name, closure)


    #handle function bodies
    def func_body(self, stmts, ret_expr):
        outer = self.env
        self.env = Env(outer)
        try:
            for s in stmts:
                self.visit(s)
            return self.visit(ret_expr)
        finally:
            self.env = outer

    #function calls
    def call(self, func_expr, arg_expr):
        closure = self.visit(func_expr)
        if not isinstance(closure, Closure):
            raise TypeError(f"{closure} is not a function")

        arg = self.visit(arg_expr)
        new_env = Env(closure.env)
        new_env.set(closure.id, arg)

        outer = self.env
        self.env = new_env
        try:
            return self.visit(closure.body)
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
    

#main
import sys
def main():
        try:
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

if __name__ == '__main__':
    main()