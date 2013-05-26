#coding=utf-8
from Decorator import Decorator
import site_helper as sh

# 记录用户post时的相关信息，可以指定多个key和value
# key表示需要保存的字段名称，value为保存的值类型
# 这些value会先在web.ctx.env中查找，如果找不到就在sh.session中查找
# 不要让data中的值优先于自动记录值，以免作弊

class RecordRequestInfo(Decorator):
    '''
    decorator = [
        ('RecordRequestInfo', dict(ip='ip', user_agent='HTTP_USER_AGENT', referrer='HTTP_REFERER') ),
    ]
    '''

    def insert(self, data):
        return self.model.insert(self.__writeInfo(data))

    def update(self, item_id, data):
        return self.model.update(item_id, self.__writeInfo(data))

    def __writeInfo(self, data):
        data = sh.copy(data)
        for key, value in self.arguments.items():
            if sh.getEnv(value, None):
                data[key] = sh.getEnv(value)
            elif sh.session.get(value, None):
                data[key] = sh.session.get(value)
        return data
