#!coding=utf-8
'''
用于测试app的基类，子类请使用appTestSetUp和appTestTearDown代替setUp和tearDown
子类可以使用self.get、self.post函数向app程序发起request

当app程序运行时如果抛出异常则会把异常信息输出到app_errors
然后，在每个测试函数完成后由tearDown检查是否有error，若有则抛出原错误信息，测试失败
如果不给TestApp提供app_errors参数，则TestApp将可能会抛出难以阅读的异常信息
当app.py发生错误时，TestApp可能会对app.py发起多次请求
'''
import unittest
import StringIO
import web
from paste.fixture import TestApp
from app import app as _app
import site_helper as sh

app_errors = StringIO.StringIO()
app = TestApp(_app.wsgifunc(), extra_environ={'wsgi.errors': app_errors})

# 用于默认注册\登录的用户信息
default_user = dict(email='test@zarkpy.com', password='123456', name='zarkpy')

# 因为app在post时不能准确地向webpy程序传递参数，这可能是一个bug, 为paste.fixture hack
def hackForInputs(f):
    def newInputs():
        if web.ctx.env.get('wsgi.input.zarkpy.post.hack', None):
            return web.ctx.env.get('wsgi.input.zarkpy.post.hack')
        else:
            return f()
    return newInputs
sh.inputs = hackForInputs(sh.inputs)

class AppTest(unittest.TestCase):

    def appTestSetUp(self):
        pass

    def appTestTearDown(self):
        pass

    def setUp(self):
        self.appTestSetUp()
        app_errors.truncate(0)

    def tearDown(self):
        self.appTestTearDown()
        error_msg = app_errors.getvalue()
        if error_msg:
            raise Exception(error_msg)

    def get(self, url, params={}, extra_environ=None):
        environ = {'REQUEST_URI': sh.paramsToUrl(url, params)}
        if extra_environ:
            environ.update(extra_environ)

        res = app.get(url, params, extra_environ=environ, expect_errors=True)

        if res.status == 200:
            return str(res.body)
        if res.status == 303:
            return ''
        else:
            raise Exception("Request Error %d" % res.status + res.errors)

    def post(self, url, params={}, extra_environ=None):
        assert(isinstance(params, (dict, web.Storage)))
        environ = {'REQUEST_URI': url, 'CONTENT_TYPE': 'text/plain; charset=utf-8', }
        if extra_environ:
            environ.update(extra_environ)
        if not isinstance(params, web.Storage):
            params = sh.storage(params)
        # hack for use paste.fixture module test app.py
        environ['wsgi.input.zarkpy.post.hack'] = params

        res = app.post(url, params, extra_environ=environ, expect_errors=True)

        if res.status == 200:
            return str(res.body)
        if res.status == 303:
            return ''
        else:
            sh.printObject(res)
            raise Exception("Request Error %d" % res.status + res.errors)

    def register(self, email='', name='', password='', params={}, login=True):
        params['email'] = email if email else default_user['email']
        params['name'] = name if name else default_user['name']
        params['password'] = password if password else default_user['password']
        if not sh.model('User').getByEmail(params['email']):
            self.post('/api/user/register', params)

    def login(self, email='', password=''):
        params = {'action': 'login'}
        params['email'] = email if email else default_user['email']
        params['password'] = password if password else default_user['password']
        return sh.loadsJson(self.post('/api/user/profile', params)).is_login

    def logout(self):
        self.post('/api/user/profile', {'action':'logout'})

    def isLogin(self):
        return sh.loadsJson(self.post('/api/user/profile', {'action':'isLogin'})).is_login
    
