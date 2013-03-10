#!coding=utf-8
# ../../api/Delete.py
import site_helper as sh
from .. import AppTest

db = sh.getDBHelper()
api_url = '/api/insert'

class TestInsert(AppTest.AppTest):

    def appTestSetUp(self):
        db.executeQuery('delete from %s' % 'UserForgetPassword')
        db.executeQuery('delete from %s' % 'SiteConfig')

    def test_POST(self):
        model = sh.model('UserForgetPassword')
        my_id = self.register()
        res = self.get(api_url, {'model_name': 'UserForgetPassword', 'code': 'c'})
        res = sh.loadsJson(res)
        # 成功插入数据
        item = model.get(res.new_id)
        self.assertIsNotNone(item)
        self.assertEqual(item.code, 'c')
        # 自动写入Userid
        self.assertEqual(item.Userid, my_id)
        # 不能自定义Userid
        res = self.get(api_url, {'model_name': 'UserForgetPassword', 'code': 'c', 'Userid': 1})
        res = sh.loadsJson(res)
        self.assertFalse(res.success)
        # 不登录的话是不能插入数据的
        old_count = model.getCount()
        self.logout()
        res = self.get(api_url, {'model_name': 'UserForgetPassword', 'code': 'c'})
        res = sh.loadsJson(res)
        self.assertEqual(old_count, model.getCount())
        self.assertFalse(res.success)
        self.assertFalse(res.has_key('new_id'))
