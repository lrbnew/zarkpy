#coding=utf-8
import site_helper as sh

# model装饰器的基类，基类装饰器如果重写model的函数，必须保持接口完全一致

class Decorator:

    # 构造函数，比方说，有一个model的实例a，传给此构造函数得到b
    # b可以重写a的函数f，并在重写的新函数f中添加新功能，然后再在f中引用a原来的函数
    # 这样即增加了新功能，又不影响原函数的运行
    # 当引用b没有的函数时，b会尝试在a中查找，因此表面上看b给a添加了某些函数
    def __init__(self, model, arguments):
        assert(isinstance(arguments, dict))
        self.model = model
        self._getRealModel()._decorator = self
        self.arguments = sh.storage(arguments)

    def __getattr__(self, attr):
        return getattr(self.model, attr)

    def _getRealModel(self):
        return self.model._getRealModel() if isinstance(self.model, Decorator) else self.model

    def _getModelTableName(self):
        return self._getRealModel().table_name
