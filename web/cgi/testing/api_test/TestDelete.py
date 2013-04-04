#coding=utf-8
# ../../api/Delete.py
import site_helper as sh
from .. import AppTest

db = sh.getDBHelper()
api_url = '/api/delete'

class TestDelete(AppTest.AppTest):

    def appTestSetUp(self):
        db.executeQuery('delete from %s' % 'UserForgetPassword')
        db.executeQuery('delete from %s' % 'SiteConfig')

    def test_POST(self):
        f_model = sh.model('UserForgetPassword')
        my_id = self.register()
        # 设置Userid后便可以删除
        new_id = f_model.insert(dict(Userid=my_id, code='c'))
        self.assertIsNotNone(f_model.get(new_id))
        data = {'model_name': 'UserForgetPassword', 'model_id': new_id}
        self.get(api_url, data)
        self.assertIsNone(f_model.get(new_id))
        # 删除不存在的数据会返回True，但是affected等于0
        res = self.get(api_url, data)
        res = sh.loadsJson(res)
        self.assertTrue(res.success)
        self.assertEqual(res.affected, 0)
        # 如果没有登录的话，是不能删除的
        data['model_id'] = f_model.insert(dict(Userid=my_id, code='c'))
        self.logout()
        res = self.get(api_url, data)
        res = sh.loadsJson(res)
        self.assertFalse(res.success)
        # 不能删除别人的数据
        my_id = self.register()
        new_id = f_model.insert(dict(Userid=my_id+1, code='c'))
        data['model_id'] = new_id
        res = self.get(api_url, data)
        res = sh.loadsJson(res)
        self.assertFalse(res.success)
        # 如果没有Userid属性的话，是不能删除的
        s_model = sh.model('SiteConfig')
        new_id = s_model.insert(dict(name='n', value='v'))
        res = self.get(api_url, {'model_name': 'SiteConfig', 'model_id': new_id})
        res = sh.loadsJson(res)
        self.assertFalse(res.success)
        self.assertIsNotNone(s_model.get(new_id))
