from lark import Lark, v_args, UnexpectedInput

#definition of grammar

grammar = """
    ?start: alt

    ?alt: seq ("|" seq)*
        | seq

    ?seq: rep (rep)*
        | rep

    rep: atom "*"
        | atom

    atom: "(" alt ")"
        | LETTER

    %import common.LETTER
    %import common.WS
    %ignore WS
"""


#creating the parser object
parser = Lark(grammar)

#example input
input_string = input("Enter an RE: ")

#print the parsed input with error handling
try:
    parse_input = parser.parse(input_string)
    print(parse_input.pretty())

except UnexpectedInput as e:
    print(f"No terminal matches '*' in the current parser context, at line {e.line}, column {e.column}")
    print(e.get_context(input_string))
