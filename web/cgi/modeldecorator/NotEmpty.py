#coding=utf-8
from Decorator import Decorator

# 断言insert和update的数据的某些字段必须存在，且不能为None和空字符串
# 在not_empty_attrs中设置需要验证的字段名称即可，比如 not_empty_attrs=['email','name','password']

class NotEmpty(Decorator):
    ''' decorator = [
        ('NotEmpty', dict(not_empty_attrs=[]) ),
    ] '''

    def insert(self, data):
        self.__NoNoneValidate(data, 'insert')
        return self.model.insert(data)

    def update(self, item_id, data):
        self.__NoNoneValidate(data, 'update')
        return self.model.update(item_id, data)

    def __NoNoneValidate(self, data, action):
        for k in self.arguments.not_empty_attrs:
            if action == 'insert':
                assert data.has_key(k), '缺少插入的数据%s' % k
                assert data[k] is not None, '插入的%s数据不能为None' % k
                if isinstance(data[k], str):
                    assert data[k].strip(), '插入的%s数据不能为空' % k
            elif action == 'update':
                if data.has_key(k):
                    assert data[k] is not None, '插入的%s数据不能为None' % k
                    assert data[k].strip(), '插入的%s数据不能为空' % k
