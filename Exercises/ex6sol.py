#Rayne Allen
#PSU ID: 963230784

# Exercise 6.1
def currying(f):
    #first inner function that takes the first argument
    def curried(x):
        #second inner function to take the second argument
        def inner(y):
            return f(x, y)
        return inner
    return curried


#normal usage
def add(x, y):
    return x + y

print(add(2, 3))

#curried function
add_curried = currying(add)

print(add_curried(2)(3))


# Exercise 6.2

#returning a function that applies function f to its input k times
def ktimes(f, k):
    def inner(x):
        result = x
        for i in range(k):
            result = f(result)
        return result
    return inner

#testing
def incr(x):
    return x + 1


ktimes_0 = ktimes(incr, 0)
print(ktimes_0(5))

ktimes_2 = ktimes(incr, 2)
print(ktimes_2(5))

ktimes_5 = ktimes(incr, 5)
print(ktimes_5(5))


# Exercise 6.3

#apply function f to each element in the terable and return the result
def mymap(f, itr):
    #determine the input type
    if type(itr) == list:
        return [f(x) for x in itr]
    elif type(itr) == tuple:
        return tuple([f(x) for x in itr])
    elif type(itr) == set:
        return set([f(x) for x in itr])
    else:
        return None

print(mymap(lambda x: x + 1, [1, 2, 3]))
print(mymap(lambda x: x + 1, (1, 2, 3)))
print(mymap(lambda x: x + 1, {1, 2, 3}))
print(mymap(str.upper, 'hello world'))


# Exercise 6.4
'''
For fib.c, it seems like the recursive function will still have function calls in the assembly. I think this because 
the function relies on finding fib(n-1) and fib(n-2). Overlapping subproblems  will make the recursive element take up a lot of memory
real estate as n grows.

for fibT.c, the recursive call to helper doesn't appear in the assemmbly code. This is because the helper function is tail recursive. 
Using tail recursion allows the compiler to optimize the code and avoid the overhead of recursive function calls.



'''