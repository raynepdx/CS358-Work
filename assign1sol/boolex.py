# <Rayne Allen>
#

# CS358 Fall'24 Assignment 1 (Part A)
#
# BoolEx - a Boolean expression language

from lark import Lark, v_args
from lark.visitors import Interpreter

# 1. Grammar
#
grammar = """

    ?orex: orex "or" andex -> orop // orex can be either 'or' of two andex's or just an andex
        | andex
    
    ?andex: andex "and" atom -> andop // andex can be either 'and' of two atoms or just an atom
        | atom

    ?atom: "not" atom -> notop // atom can be either 'not' of an atom or just a value
        | "(" orex ")"
        | "True" -> truev
        | "False" -> falsev


    %import common.WS_INLINE
    %ignore WS_INLINE

"""
# Parser
#
# E.g. (True or not False) and True
#      => andop  
#           orop
#             truev
#             notop
#               falsev
#           truev
#
parser = Lark(grammar, start='orex')

# 2. Interpreter
#
# E.g. (for the above example)
#      => True
#
@v_args(inline=True)
class Eval(Interpreter):

    def orop(self, left, right):
        #if left is true, return true without evaluating right
        return self.visit(left) or self.visit(right)
    
    def andop(self, left, right):
        #if left is false, return false without evaluating right
        return self.visit(left) and self.visit(right)
    
    def notop(self, val):
        #NOT operation
        return not self.visit(val)
    
    def truev(self):
        return True
    
    def falsev(self):
        return False


# 3. Convert the AST to a list form
#
# E.g. (for the above example)
#      => ['and', ['or', 'True', ['not', 'False']], 'True']
#
@v_args(inline=True)
class toList(Interpreter):

    def orop(self, left, right):
        return ['or', self.visit(left), self.visit(right)] #represent OR as ['or', left, right]
    
    def andop(self, left, right):
        return ['and', self.visit(left), self.visit(right)] #represent AND as ['and', left, right]
    
    def notop(self, val):
        return ['not', self.visit(val)] #represent NOT as ['not', val]
    
    def truev(self):
        return 'True'   #represent True as string
    
    def falsev(self):
        return 'False'  #represent False as string


# 4. Convert a nested list to a string form
#
# E.g. (for the above example)
#      => (and (or True (not False)) True)
#
def strForm(lst):

    #if the element is a list, recursively call strForm to convert the elements into a string, surrounded by parentheses
    #if the element is a string, return the string

    if isinstance(lst, list):
        return f"({lst[0]} {' '.join(strForm(x) for x in lst[1:])})" #recursively format the list as a string
    
    return str(lst) #return the string as a base case


def main():
    while True:
        try:
            expr = input("Enter a bool expr: ")
            tree = parser.parse(expr)
            lst = toList().visit(tree)
            print(expr)
            print(tree.pretty(), end="")
            print("tree.Eval() =", Eval().visit(tree))
            print("tree.toList() =", lst)
            print("strForm() =", strForm(lst))
            print()
        except EOFError:
            break
        except Exception as e:
            print("***", e)

if __name__ == '__main__':
    main()
