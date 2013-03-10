#!coding=utf-8
# ../../api/Delete.py
import site_helper as sh
from .. import AppTest

db = sh.getDBHelper()
api_url = '/api/get'

class TestGet(AppTest.AppTest):

    def appTestSetUp(self):
        db.executeQuery('delete from %s' % 'SiteConfig')

    def test_POST(self):
        model = sh.model('SiteConfig')
        new_id = model.insert({'name': 'n', 'value': 'v' })
        res = self.get(api_url, {'model_name':'SiteConfig', 'model_id': new_id})
        res = sh.loadsJson(res)
        self.assertEqual(res.id, new_id)
        self.assertEqual(res.SiteConfigid, new_id)
        self.assertEqual(res.name, 'n')

        res = self.get(api_url, {'model_name':'SiteConfig', 'model_id': new_id+1})
        res = sh.loadsJson(res)
        self.assertEqual(res, 'None')
