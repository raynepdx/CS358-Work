class Env(dict):
    #a list for keeping previous environments
    prev_envs = []


    def open_scope(self):
        #push the current env to the prev list, return a new empty env
        self.prev_envs.append(self.copy()) #save a copy of the current env
        return Env() #return a new empty env
    

    def close_scope(self):
        #pop off the top env from the prev list, return this env
        if not self.prev:
            raise Exception("No previous environment to return to")
        return self.prev_envs.pop() #restore the previous env
    

    def extend(self, x, y):
        #add an entry to the current env, raise exception for redefining
        if x in self:
            raise Exception(f"Variable {x} already defined in the current scope")
        self[x] = y


    def lookup(self, x):
        #search for a variable starting from the current env, and continue with prev
        if x in self:
            return self[x]
        
        #check previous envs
        for scope in reversed(self.prev_envs):
            if x in scope:
                return scope[x]
            
        raise Exception(f"Variable {x} not found in the current scope or any previous scope")
    

    def update(self, x, y):
        #search for a variable and update its value, raise exception if not found
        if x in self:
            self[x] = y
            return
        
        #check previous envs
        for scope in reversed(self.prev_envs):
            if x in scope:
                scope[x] = y
                return
            
        raise Exception(f"Variable {x} not found in the current scope or any previous scope")
    

    def display(self, message):
        #show the content of all envs
        print(message, self, self.prev_envs)



#main function to test code
def main():
    global env #global env for testing
    env = Env() #always pointing to the current env

    env.extend("x", 0) #scope 0
    env.extend("y", 10)
    env.display("Scope 0:")

    env = env.open_scope() #scope 1
    env.update("x", 5)
    env.extend("x", 1)
    env.display("Scope 1:")

    x = env.lookup("x")
    y = env.lookup("y")

    print("x, y =", x, y, "(should be 1, 10)")

    env = env.open_scope() #scope 2
    env.update("y", 11)
    env.extend("y", 12)
    env.display("Scope 2:")

    x = env.lookup("x")
    y = env.lookup("y")

    print("x, y =", x, y, "(should be 1, 12)")

    env = env.close_scope() #scope 1
    env = env.close_scope() #scope 0
    env.display("Scope 0:")

    x = env.lookup("x")
    y = env.lookup("y")

    print("x, y = ", x, y, "(should be 5, 11)")


    if __name__ == "__main__":
        main()