#!coding=utf-8
import unittest
import site_helper as sh
from .. import AppTest

db = sh.getDBHelper()

class TestRecordRequestInfo(AppTest.AppTest):

    def test_insert(self):
        data = dict(data_name='User', data_id=1, model_name='Image')
        self.register()
        #self.get('/api/user/register', data)
        #r = self.post('/cgi/insert')
        #help(self.app.post)
        #r = self.app.get('/cgi/index')
        #print r.headers
        #help(r)
