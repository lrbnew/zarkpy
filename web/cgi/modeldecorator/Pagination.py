#coding=utf-8
import web
import math
from Decorator import Decorator
import site_helper as sh

# 分页装饰, paging_key为页码属性名，paging_volume为每页数据量，paging指明是否自动开启分页功能

class Pagination(Decorator):
    ''' decorator = [
        ('Pagination', dict(paging_key='page_num', paging_volume=20, paging=True) ),
    ] '''

    # 通过给env添加limit来实现分页
    def all(self, env=None):
        env = sh.copy(env) if env is not None else {}
        if not env.has_key('limit') and env.get('paging', self.arguments.paging):
            env['limit'] = self.__getLimit(self.__getPageNum(env), self.__getVolume(env))
        return self.model.all(env)

    # 对已有数据进行分页(切片)
    def pagingDatas(self, datas, page_num=None, volume=None):
        if page_num is None:
            page_num = web.input().get(self.arguments.paging_key, 1)
        if volume is None:
            volume = self.arguments.paging_volume
        if page_num and volume:
            start, length = self.__getLimit(page_num, volume)
            return datas[start:start+length]
        else:
            return datas

    # 返回分页的前端代码，需要结合zarkfx使用
    def getPaginationHtml(self, env=None):
        env = sh.copy(env) if env is not None else {}
        return '<div fx="pagination[style=default;max=%d;displaycount=10;firsttext=第一页;lasttext=末页;]"></div>' % max(1, math.ceil(self.getCount(env) * 1.0 / self.__getVolume(env))) if env.get('paging', self.arguments.paging) else ''
    
    def __getLimit(self, page_num, volume):
        return (int(volume) * (int(page_num) -1), int(volume))

    def __getPageNum(self, env):
        key = self.arguments.paging_key
        return int(env.get(key, web.input().get(key, 1)))

    def __getVolume(self, env):
        return int(env.get('paging_volume', self.arguments.paging_volume))
