# <Rayne Allen>
#

# CS358 Fall'24 Assignment 2 (Part A)
#
# Expr - an expression language with arithmetic, logical, and 
#        relational operations
#

from lark import Lark, v_args
from lark.visitors import Interpreter

# Grammar
#
grammar = """
  ?start: expr

  ?expr: expr "or" and_expr -> or_expr
         | and_expr

    ?and_expr: and_expr "and" rel_expr -> and_expr
                | rel_expr

    ?rel_expr: rel_expr "<" arith_expr -> lt
                | rel_expr ">" arith_expr -> gt
                | rel_expr "<=" arith_expr -> le
                | rel_expr ">=" arith_expr -> ge
                | rel_expr "==" arith_expr -> eq
                | rel_expr "!=" arith_expr -> ne
                | arith_expr

    ?arith_expr: arith_expr "+" term -> add
                | arith_expr "-" term -> sub
                | term

    ?term: term "*" atom -> mul
            | term "/" atom -> div
            | atom

    ?atom: "not" atom -> not_expr
            | "(" expr ")"
            | "True" -> truev
            | "False" -> falsev
            | NUM -> num

    %import common.INT -> NUM
    %ignore " "   
"""

parser = Lark(grammar)

# Interpreter
#
@v_args(inline=True)
class Eval(Interpreter):
    def num(self, val):  return int(val)
    def add(self, x, y): return Eval().visit(x) + Eval().visit(y)
    def sub(self, x, y): return Eval().visit(x) - Eval().visit(y)
    def mul(self, x, y): return Eval().visit(x) * Eval().visit(y)
    def div(self, x, y): return Eval().visit(x) // Eval().visit(y)

    def truev(self): return True
    def falsev(self): return False

    #logical operations
    def or_expr(self, x, y): return Eval().visit(x) or Eval().visit(y)
    def and_expr(self, x, y): return Eval().visit(x) and Eval().visit(y)
    def not_expr(self, x): return not Eval().visit(x)

    #relational operations
    def lt(self, x, y): return Eval().visit(x) < Eval().visit(y)
    def gt(self, x, y): return Eval().visit(x) > Eval().visit(y)
    def le(self, x, y): return Eval().visit(x) <= Eval().visit(y)
    def ge(self, x, y): return Eval().visit(x) >= Eval().visit(y)
    def eq(self, x, y): return Eval().visit(x) == Eval().visit(y)
    def ne(self, x, y): return Eval().visit(x) != Eval().visit(y)

def main():
    try:
        prog = input("Enter an expr: ")
        tree = parser.parse(prog)
        print(prog)
        print(tree.pretty(), end="")
        print(Eval().visit(tree))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
