from lark import Lark, v_args
from lark.visitors import Interpreter

#grammar allowing for chained relational operators
grammar = """
    start: expr

    ?expr: arith_expr (rel_op arith_expr)+ -> chained_compare
            | arith_expr

    ?arith_expr: arith_expr "+" term -> add
                | arith_expr "-" term -> sub
                | term

    ?term: term "*" atom -> mul
            | term "/" atom -> div
            | atom

    ?atom: NUM -> num
            | ID -> var
            | "(" expr ")"

    rel_op: "<" | "<=" | ">" | ">=" | "==" | "!="

    %import common.WORD   -> ID
    %import common.INT    -> NUM
    %import common.WS
    %ignore WS
"""

parser = Lark(grammar)

#interpreter for chained relational operators
@v_args(inline=True)
class Eval(Interpreter):
    def __init__(self):
        super().__init__()
        self.env = {} #initialize environment

    def num(self, val):  return int(val)
    def var(self, name): return self.env.get(str(name), 0)
    def assign(self, name, value):
        self.env[str(name)] = self.visit
        return self.env[str(name)]
    
    def add(self, x, y): return self.visit(x) + self.visit(y)
    def sub(self, x, y): return self.visit(x) - self.visit(y)
    def mul(self, x, y): return self.visit(x) * self.visit(y)
    def div(self, x, y): return self.visit(x) // self.visit(y)

    #chained comparison operations
    def chained_compare(self, first, *ops_and_vals):
        current_val = self.visit
        i = 0

        while i < len(ops_and_vals) - 1:
            op = ops_and_vals[i]
            next_val = self.visit(ops_and_vals[i+1])
            if op == "<" and not (current_val < next_val):
                return False
            elif op == "<=" and not (current_val <= next_val):
                return False
            elif op == ">" and not (current_val > next_val):
                return False
            elif op == ">=" and not (current_val >= next_val):
                return False
            elif op == "==" and not (current_val == next_val):
                return False
            elif op == "!=" and not (current_val != next_val):
                return False
            current_val = next_val
            i += 2
            return True
        

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