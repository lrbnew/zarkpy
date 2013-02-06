#coding=utf-8
'''因为python已经有一个test库了，所以为了避免import冲突，起名testing'''

# 测试时，可能需要使用一个临时的model, 可以用此函数向sh.model注册新的model
# 但不要把此功能用于正式代码，否则会增加程序的不透明性
def registerModel(_class):
    import model
    _class().createTable()
    class_name = str(_class).rpartition('.')[2] if '.' in str(_class) else str(_class)
    exec "model.%s = _class" %  class_name
