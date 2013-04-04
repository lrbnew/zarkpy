#coding=utf-8
import unittest
import site_helper as sh

db = sh.getDBHelper()

class TestPagination(unittest.TestCase):

    def setUp(self):
        conf_model = sh.model('SiteConfig')
        db.executeQuery('delete from %s' % conf_model.table_name)

    def test_all(self):
        decorator = [ ('Pagination', dict(paging_key='page_num', paging_volume=20, paging=False) ), ]
        conf_model = sh.model('SiteConfig', decorator)
        for i in range(100):
            conf_model.insert(dict(name=i, value=i))
        # 不使用分页
        self.assertEqual(len(conf_model.all()), 100)
        items = conf_model.all({'paging_volume': 15, 'page_num': 2})
        self.assertEqual(len(items), 100)
        # 显示调用分页, 获得20个数据
        items = conf_model.all({'paging': True, 'page_num': 2})
        self.assertEqual(len(items), 20)
        self.assertEqual(items[0].value, '20')
        # 显示指定每页个数
        items = conf_model.all({'paging': True, 'paging_volume': 15, 'page_num': 2})
        self.assertEqual(len(items), 15)
        self.assertEqual(items[0].value, '15')

    def test_pagingDatas(self):
        decorator = [ ('Pagination', dict(paging_key='page_num', paging_volume=20, paging=False) ), ]
        conf_model = sh.model('SiteConfig', decorator)
        for i in range(100):
            conf_model.insert(dict(name=i, value=i))
        items = conf_model.all()
        self.assertEqual(len(items), 100)
        # 使用pagingDatas返回第15到30个数据
        sub_items = conf_model.pagingDatas(items, 2, 15)
        self.assertEqual(len(sub_items), 15)
        self.assertIs(items[15], sub_items[0])
