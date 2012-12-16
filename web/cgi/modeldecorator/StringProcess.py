#coding=utf-8
from Decorator import Decorator
import site_helper as sh

# 字符串处理，可以有多个key和values，每个key对应一个str类的函数，比如strip、lower等
# 每个values是一个由多个属性名称组成的list，表示要处理的数据

class StringProcess(Decorator):
    ''' decorator = [
        ('StringProcess', dict(strip=['title']) )
    ] '''

    def insert(self, data):
        return self.model.insert(self.__processData(data))

    def update(self, item_id, data):
        return self.model.update(item_id, self.__processData(data))

    def __processData(self, data):
        data = sh.copy(data)
        for key, values in self.arguments.items():
            assert(hasattr(str, key))
            assert(isinstance(values, list) or isinstance(values, tuple))
            for v in values:
                if data.has_key(v):
                    data[v] = getattr(str, key)(sh.unicodeToStr(data[v]))
        return data
