import functools
def des(i): # this is the "decorator creator", called with des(1)
    def deco(func): # this is returned and is the real decorator, called at function definition time
        @functools.wraps(func) # sugar
        def new_func(*a, **k): # and this is the function called on execution.
            if i == 1:
                raise Exception # I hope this is just for testing... better create a new exception for this
            else:
                return func(*a, **k)
        return new_func
    return deco

@des(2)
def func():
    print("!!")

if __name__ == '__main__':
    try:
        func()
    except Exception:
        print('error')
