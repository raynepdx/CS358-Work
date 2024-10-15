from lark import Lark, v_args

grammar = """
    ?start: expr
    ?expr: expr "+" term -> add
        | expr "-" term -> sub
        | term
    ?term: term "*" atom -> mul
        | term "/" atom -> div
        | atom
    ?atom: "(" expr ")"
        | NUMBER        -> num

    %import common.NUMBER
    %import common.WS
    %ignore WS
"""