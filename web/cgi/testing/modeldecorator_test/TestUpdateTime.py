#!coding=utf-8
import unittest
import datetime
import site_helper as sh

db = sh.getDBHelper()

class TestUpdateTime(unittest.TestCase):

    def setUp(self):
        model = sh.model('ForTestUpdateTime')
        db.executeQuery('delete from %s' % model.table_name)

    def test_insert_update(self):
        # 得到开始时间
        start = self._getCurrentTime()
        # 插入数据
        model = sh.model('ForTestUpdateTime')
        new_id = model.insert(dict(title='something'))
        item = model.get(new_id)
        # 时间大于start
        t1 = item.t
        self.assertIsNotNone(t1)
        self.assertGreaterEqual(t1, start)
        # update 数据后时间可能会变得更大
        model.update(new_id, dict(title='something'))
        t2 = model.get(new_id).t
        self.assertGreaterEqual(t2, t1)
        # 获得结束时间
        end = self._getCurrentTime()
        # 结束时间大于t2
        self.assertGreaterEqual(end, t2)

    # 获得当前时间，精确到秒
    def _getCurrentTime(self):
        t = datetime.datetime.now()
        return datetime.datetime(t.year, t.month, t.day, t.hour, t.minute, t.second)


# 用于测试UpdateTime的类
from model import Model
class ForTestUpdateTime(Model):
    table_name      = 'ForTestUpdateTime'
    column_names    = ['title', 'created', ]
    test_decorator  = [
        ('UpdateTime', dict(attr_name='t') ),
    ]
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            title       varchar(100)  charset utf8 not null default '',
            t           timestamp not null,
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''

from .. import registerModel
registerModel(ForTestUpdateTime)
