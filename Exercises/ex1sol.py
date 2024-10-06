#Rayne Allen, PSU ID 963230784

#Exercise 1.1

#Using only string operations, this function returns true if a string argument is a palindrome, and false otherwise.
def palindrome1(s: str) -> bool:
    return s == s[::-1]

#Using a loop, this function returns true if a string argument is a palindrome, and false otherwise.
def palindrome2(s: str) -> bool:
    left = 0
    right = len(s) -1

    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True




#Exercise 1.2

def newstack() -> list:
    return []

def newqueue() -> list:
    return []

def push(s, x):
  s.append(x)
  return s

def pop(s):
    while s:
        s.pop()
        return s
    
def enqueue(q, x):
    if q.isFull():
        print("Queue is full")
        return
    q.rear = (q.rear + 1) % (q.size)
    q.items[q.rear] = x
    q.size += 1
    print(str(x) + " enqueued to queue")

def dequeue(q):
    if q.isEmpty():
        print("Queue is empty")
        return
    print(str(q.items[q.front]) + " dequeued from queue")
    q.front = (q.front + 1) % (q.size)
    q.size -= 1



#Exercise 1.3

def fac1(n: int):
    if n < 0:
        return None
    if n == 0 or n == 1:
        return 1
    return n * fac1(n - 1)

def fac2(n: int):
    if n < 0 :
        return None
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result



#Exercise 1.4
'''a)
The ^(XOR) operator has left-to-right associativity and takes precedence over the other operators. 
Then, the * operator has left-to-right associativity and takes precedence over the + operator. 
Then, the + operator has left-to-right associativity. The - operator has left-to-right associativity and takes precedence last.'''
'''After we establish that, we evaluate 3 ^ 4 first, then 2 * (3 ^ 4), then 1 + (2 * (3 ^ 4)), then (1 + (2 * (3 ^ 4))) - 5'''
'''3 ^ 4 = 7,
   2 * 7 = 14,
   1 + 14 = 15,
   15 - 5 = 10
   
   with that in mind, we can see that the result of the expression is 10, and the AST is expressed in linear text as: [- [ + 1 [* 2 [^ 3 4]]] 5]'''


'''b)
if - (subtraction) has the highest precedence, followed by addition, then multiplication, then the bitwise XOR operator with the lowest precedence, the expression would be evaluated as follows:
    first, -5 is evaluated, followed by 1 + (-5), then (1 + (-5)) * 2, then ((1 + (-5)) * 2) ^ 3.  
    This would come out to [^ [* [+ 1 [ -5]] 2] 3]
    -5 = -5, 1 + (-5) = -4, -4 * 2 = -8, -8 ^ 3 = -5, so the expression woulde come out to -5    '''



