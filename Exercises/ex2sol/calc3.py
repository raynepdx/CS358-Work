#this file covers the first two parts of the exercise. calc1d_interpreter.py uses the lark interpreter from slide 17 to interpret the parse tree. calc2b_revised.py uses the ASTNode class from ex1sol.py to interpret the parse tree. The ASTNode class is more flexible and can be used to interpret more complex expressions than the lark interpreter. The lark interpreter is easier to use and requires less code to interpret the parse tree. The ASTNode class is more object-oriented and can be extended to support more operations and expressions. The lark interpreter is more functional and can be used to parse and interpret expressions in a single step. Both approaches have their strengths and weaknesses, and the choice between them depends on the complexity and requirements of the project.

from lark import Lark, v_args, Tree, Token
from lark.visitors import Interpreter
from calc1d_interpreter import grammar #import the grammar from calc1d_interpreter.py

@v_args(inline=True) #makes the visitor methods receive tree children as args

class Eval(Interpreter): #this class will interpret the parse tree
    def num(self, val): #this method will interpret the num rule
        return int(val) #converts the value from the tree to an integer, and return said integer
    
    def add(self, left, right): #handles the 'add' rule
        return self.visit(left) + self.visit(right) #recursively visits the left and right children of the tree, and returns the sum of the results
    
    def sub(self, left, right): #handles the 'sub' rule
        return self.visit(left) - self.visit(right) #recursively visits the left and right children of the tree, and returns the difference of the results
    
    def numNodes(self, tree): #count the number of nodes in the tree
        if isinstance(tree, Tree): #if the tree is an instance of Tree from the lark library
            return sum(self.numNodes(child) for child in tree.children) + 1
        
        elif isinstance(tree, Token): #using the Token class from lark to see if the current node is a leaf
            return 1
        return 0
    
    def count1s(self, tree): #count the number of leaves with a value of 1
        if isinstance(tree, Tree): #if the tree is an instance of Tree from the lark library
            return sum(self.count1s(child) for child in tree.children)
        
        elif isinstance(tree, Token): #using the Token class from lark to see if the current node is a leaf
            return 1 if tree.type == 'NUMBER' and tree.value == '1' else 0
        
        return 0
    
    def toList(self, tree): #function to convert the tree to a list representation
        if isinstance(tree, Tree): #if the tree is an instance of Tree from the lark library
            return [tree.data] + [self.toList(child) for child in tree.children]
        
        elif isinstance(tree, Token): #using the Token class from lark to see if the current node is a leaf
            return int(tree.value) if tree.type == 'NUMBER' else tree.value
        
        return None
    
parser = Lark(grammar) #create a parser object using the grammar

#main function
def main():
    while True: #read-eval-print loop
        try:
            prog = input("Enter an expression: ") #ask user for input
            tree = parser.parse(prog) #parse the input into a syntax tree
            print(tree.pretty()) #print the tree in a readable format (for debugging purposes)
            eval_instance = Eval() #create an instance of the Eval class to interpret the tree
            result = eval_instance.visit(tree) #interpret the tree and get the result
            node_count = eval_instance.numNodes(tree) #count the number of nodes in the tree
            leaf_count_with_one = eval_instance.count1s(tree) #count the number of leaves with a value of 1
            tree_list = eval_instance.toList(tree) #convert the tree to a list representation
            print(f"tree.Eval() = : {result}") #print the result
            print(f"tree.numNodes() = : {node_count}") #print the number of nodes in the tree
            print(f"tree.count1s() = : {leaf_count_with_one}") #print the number of leaves with a value of 1
            print(f"tree.toList() = : {tree_list}") #print the list representation of the tree

        except EOFError: #if the user presses Ctrl+D, exit the loop (I can't seem to get this to work. Feedback would be greatly appreciated)
            print("\nExiting...")
            break

        except KeyboardInterrupt: #if the user presses Ctrl+C, exit the loop
            print("\nExiting...")
            break

        except Exception as e: #catch any other exceptions
            print(e)

if __name__ == '__main__':
    main()