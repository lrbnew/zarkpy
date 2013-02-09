#coding=utf-8
import datetime
from Decorator import Decorator
import site_helper as sh

''' 自动记录数据最后一次的更新时间 '''

class UpdateTime(Decorator):
    ''' decorator = [
        ('UpdateTime', dict(attr_name='updated') ),
    ] '''

    def insert(self, data):
        assert not data.has_key(self.arguments.attr_name)
        data = sh.copy(data)
        data[self.arguments.attr_name] = datetime.datetime.now()
        return self.model.insert(data)

    def update(self, item_id, data):
        assert not data.has_key(self.arguments.attr_name)
        data = sh.copy(data)
        data[self.arguments.attr_name] = datetime.datetime.now()
        return self.model.update(item_id, data)
