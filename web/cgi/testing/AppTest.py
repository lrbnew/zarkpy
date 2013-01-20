#!coding=utf-8
'''
用于测试app的基类，子类请使用appTestSetUp和appTestTearDown代替setUp和tearDown
子类可以使用self.app的get、post等函数向app程序发起request

当app程序运行时如果抛出异常则会把异常信息输出到app_errors
然后，在每个测试函数完成后由tearDown检查是否有error，若有则抛出原错误信息，测试失败
如果不给TestApp提供app_errors参数，则TestApp将可能会抛出难以阅读的异常信息
'''
import unittest
import StringIO
from paste.fixture import TestApp
from app import app as _app

app_errors = StringIO.StringIO()
app = TestApp(_app.wsgifunc(), extra_environ={'wsgi.errors': app_errors})

class AppTest(unittest.TestCase):

    def appTestSetUp(self):
        pass

    def appTestTearDown(self):
        pass

    def setUp(self):
        self.appTestSetUp()
        app_errors.truncate(0)
        self.app = app

    def tearDown(self):
        self.appTestTearDown()
        error_msg = app_errors.getvalue()
        if error_msg:
            raise Exception(error_msg)
