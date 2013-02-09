#!coding=utf-8
import unittest
import site_helper as sh

db = sh.getDBHelper()

class TestStringProcess(unittest.TestCase):

    def setUp(self):
        model = sh.model('SiteConfig')
        db.executeQuery('delete from %s' % model.table_name)

    def test_insert_update(self):
        decorator = [('StringProcess', dict(strip=['name', 'value'], lower=['value'])),]
        model = sh.model('SiteConfig', decorator)
        new_id = model.insert(dict(name=' speed ', value='FAST '))
        item = model.get(new_id)
        # 用strip删除了两边的空格, 用lower把value改为小写
        self.assertEqual(item.name, 'speed')
        self.assertEqual(item.value, 'fast')
        # update同样起作用
        model.update(new_id, dict(value=' SLOW '))
        item = model.get(new_id)
        self.assertEqual(item.value, 'slow')
