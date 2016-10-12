import time

def timeit(func):
    def wrapper(*args, **kwargs):
        t = time.time()
        func(*args, **kwargs)
        print (time.time() - t)
    return wrapper

def memoize(func):
    dic = dict()
    def wrapper(n):
        if n in dic:
            return dic[n]
        dic[n] = func(n)
        return dic[n]
    return wrapper

def staticmethod_(func):
    def wrapper(*args, **kwargs):
        try: 
            func(*args, **kwargs)
        except:
            func(*(args[1:]), **kwargs)
    return wrapper


class Meow:
   def __init__(self, word = "MEOW"):
       self.word = word
   @staticmethod_
   def say(word):
       print(word)
           

@memoize
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

@timeit
def magic(n):
    for i in range(n):
        print("MEOW")

magic(20)
print(fib(10))
#cat = Meow()
Meow().say("MEEEEOOOW")
Meow.say("PURRR")

