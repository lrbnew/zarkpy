#coding=utf-8
# ../../api/Delete.py
import site_helper as sh
from .. import AppTest

db = sh.getDBHelper()
api_url = '/api/update'

class TestUpdate(AppTest.AppTest):

    def appTestSetUp(self):
        db.executeQuery('delete from %s' % 'UserForgetPassword')
        db.executeQuery('delete from %s' % 'SiteConfig')

    def test_POST(self):
        f_model = sh.model('UserForgetPassword')
        my_id = self.register()
        # 设置Userid后便可以更新
        new_id = f_model.insert(dict(Userid=my_id, code='c'))
        self.assertIsNotNone(f_model.get(new_id))
        data = {'model_name': 'UserForgetPassword', 'model_id': new_id}
        data['code'] = 'new_code'
        res = self.get(api_url, data)
        res = sh.loadsJson(res)
        self.assertEqual(f_model.get(new_id).code, 'new_code')
        self.assertEqual(res.affected, 1)
        # 更新不存在的数据返回True，但是affected等于0
        data['model_id'] = new_id + 1
        res = self.get(api_url, data)
        res = sh.loadsJson(res)
        self.assertTrue(res.success)
        self.assertEqual(res.affected, 0)
        # 如果没有登录的话，是不能更新的
        self.logout()
        data['code'] = 'code_again'
        res = self.get(api_url, data)
        res = sh.loadsJson(res)
        self.assertFalse(res.success)
        # 不能更新别人的数据
        my_id = self.register()
        new_id = f_model.insert(dict(Userid=my_id+1, code='c'))
        data['model_id'] = new_id
        res = self.get(api_url, data)
        res = sh.loadsJson(res)
        self.assertFalse(res.success)
        # 如果没有Userid属性的话，是不能更新的
        s_model = sh.model('SiteConfig')
        new_id = s_model.insert(dict(name='n', value='v'))
        data = {'model_name': 'SiteConfig', 'model_id': new_id, 'name': 'a'}
        res = self.get(api_url, data)
        res = sh.loadsJson(res)
        self.assertFalse(res.success)
        self.assertEqual(s_model.get(new_id).name, 'n')
