
dic = {
    "users":"user"
}
print("user" in dic, "222")







s="1"
name="f1"
exec("""def {}():
    print('in func {}')
    print('in func {}')
print("out of func {}")""".format(name,name,name,name))
# f1()
def if_session(arg1):
    print(arg1, "开始装饰函数")
    if arg1 not in "123":
        print(1,"进入if")
        def inner(func):
            def wrapper(*args, **kwargs):
                print(2, "打包函数并传入参数")
                return func(*args, **kwargs) # 返回函数func(*args,**kwargs)，不运行
            return wrapper
        print(3)
        return inner
    else:
        print("no")

# 等价于
def ff(arg1, func, *args, **kwargs):
    print(arg1)
    print(1)
    print(2)
    print(3)
    return func(arg1, *args, **kwargs)

@if_session("4")
def main():
    print("good")

@if_session("5")
def main1():
    print("bad")

print(main)
print(main1)