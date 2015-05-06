def a():
    global x
    x = 1
    b()
def b():
    print x

def c():
    global y
    y = 1
def d():
    print y
def e():
    global y
    print y

def f():
    global z
    z = max
    g()
def g():
    #global z
    if z==max:
        print z