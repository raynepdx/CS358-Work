class Num:
    def __init__(self,v): self.val = v
    def add(self,other): raise NotImplementedError("add not implemented")

class Int(Num):
    def __init__(self, v):
        if not isinstance(v, int):
            raise ValueError("Int value must be an int")
        super().__init__(v)

    def add(self, other):
        if isinstance(other, Str):
            return self.val + int(other.val)
        elif isinstance(other, Int):
            return self.val + other.val
        else:
            raise TypeError("Int add called with invalid type")
    
class Str(Num):
    def __init__(self, v):
        if not isinstance(v, str):
            raise ValueError("Str value must be a str")
        super().__init__(v)

    def add(self, other):
        if isinstance(other, Str):
            return self.val + other.val
        elif isinstance(other, Int):
            return self.val + str(other.val)
        else:
            raise TypeError("Str add called with invalid type")
    
    def add(self, other):
        if isinstance(other, Str):
            return self.val + other.val
        elif isinstance(other, Int):
            return self.val + str(other.val)
        else:
            raise TypeError("Str add called with invalid type")


def add(x,y):
    if isinstance(x, Str) and isinstance(y, Str):
        return x.val + y.val
    elif isinstance(x, Num) and isinstance(y, Num):
        return int(x.val) + int(y.val)
    else:
        raise TypeError("add called with invalid types")

if __name__ == "__main__":
    ival = Int(1)
    sval = Str("2")
    sval2 = Str("3")
    print("add(ival,ival) =", add(ival,ival))
    print("add(ival,sval) =", add(ival,sval))
    print("add(sval,ival) =", add(sval,ival))
    print("add(sval,sval2) =", add(sval,sval2))
    print("ival.add(ival) =", ival.add(ival))
    print("ival.add(sval) =", ival.add(sval))
    print("sval.add(ival) =", sval.add(ival))
    print("sval.add(sval) =", sval.add(sval2))
