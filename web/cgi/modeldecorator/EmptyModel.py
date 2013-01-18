#coding=utf-8
from Decorator import Decorator
import site_helper as sh

# 空数据模式，不需要参数

class EmptyModel(Decorator):
    ''' decorator = [
        ('EmptyModel', {}),
    ] '''

    # 把datas中的None改为empty数据，非None不变
    def noneToEmpty(self, datas):
        if isinstance(datas, list) or isinstance(datas, tuple):
            return [d if d is not None else self.getEmptyData() for d in datas]
        else:
            return datas if datas else self.getEmptyData()

    # 获得一个empty数据
    def getEmptyData(self):
        data = sh.storage([(k, '') for k in self.model.column_names])
        data['__is_empty'] = True
        return data
