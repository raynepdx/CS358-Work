#------------------------------------------------------------------------------ 
# For CS358 Principles of Programming Languages, Portland State University (JL)
#------------------------------------------------------------------------------ 

import sys

class T: pass

class T0(T):
    def __init__(self,x): self.x = x

    def sum(self): return self.x
    def equal(self,other): return other.eqT0(self)
    def eqT0(self,other): return self.x == other.x
    def eqT2(self, other): return False

class T2(T):
    def __init__(self,x,left,right):
        self.x = x
        self.left = left
        self.right = right

    def sum(self):
        return self.x + self.left.sum() + self.right.sum()

    def equal(self,other):
        return other.eqT2(self)

    def eqT0(self, other): return False

    def eqT2(self,other):
        return self.x == other.x \
            and self.left.equal(other.left) \
            and self.right.equal(other.right)
    

class T3(T):
    def __init__(self, x, left, middle, right): #middle is the third child
        self.x = x
        self.left = left
        self.middle = middle
        self.right = right

    def sum(self): #sum of the three children and the node
        return self.x + self.left.sum() + self.middle.sum() + self.right.sum()
    
    def equal(self, other): #check if the other obj's eqT3 is equal to this one
        return other.eqT3(self)
    
    def eqT0(self, other): #T3 node cant be equal to T0 node
        return False
    
    def eqT2(self, other): #T3 node cant be equal to T2 node
        return False
    
    def eqT3(self, other): #compare the T3 nodes by value and children
        return self.x == other \
            and self.left.equal(other.left) \
            and self.middle.equal(other.middle) \
            and self.right.equal(other.right)
        

if __name__ == "__main__":
    t1 = T2(1,T0(2),T2(4,T0(0),T0(3)))
    t2 = T2(1,T0(2),T2(4,T0(0),T0(3)))
    t3 = T2(1,T0(2),T0(0))

    #test of a new tree structure using T3
    t4 = T3(1,T0(2),T0(0),T0(3))
    t5 = T3(1,T0(2),T0(0),T0(3))
    t6 = T3(1,T0(2),T0(3),T0(0))

    #test sum and equal methods
    print("t4.sum() =", t4.sum())
    print("t5.sum() =", t5.sum())
    print("t6.sum() =", t6.sum())
    print("t4.equal(t5):", t4.equal(t5))
    print("t4.equal(t6):", t4.equal(t6))
    
    print("t1.sum() =", t1.sum())
    print("t3.sum() =", t3.sum())
    print("t1.equal(t2):", t1.equal(t2))
    print("t1.equal(t3):", t1.equal(t3))
