from lark import Lark, Tree

# Initial grammar for the dangling-else problem
grammar = """
    stmt: "if" "expr" stmt ["else" stmt] | "other"
"""

# Initialize the parser
parser = Lark(grammar)

# Test case
test_case = "if expr if expr other else other"

# Parse the test case and print the resulting parse tree
tree = parser.parse(test_case)
print(tree.pretty())
