#coding=utf-8
'''
用于测试app的基类，子类请使用appTestSetUp和appTestTearDown代替setUp和tearDown
子类可以使用self.get、self.post函数向app程序发起request

当app程序运行时如果抛出异常则会把异常信息输出到app_errors
然后，在每个测试函数完成后由tearDown检查是否有error，若有则抛出原错误信息，测试失败
如果不给TestApp提供app_errors参数，则TestApp将可能会抛出难以阅读的异常信息
当app.py发生错误时，TestApp可能会对app.py发起多次请求

TestApp程序会自动处理cookie, 当要求"assert sh.session.is_login"时可以用AppTest
提供的各种函数请求app程序，也可以使用proxyDo模拟用户
'''
import unittest
import StringIO
import web
from paste.fixture import TestApp
from app import app as _app
import site_helper as sh
from model import ModelData

app_errors = StringIO.StringIO()
app = TestApp(_app.wsgifunc(), extra_environ={'wsgi.errors': app_errors})

# 用于默认注册\登录的用户信息
default_user = dict(email='test@zarkpy.com', password='123456', name='zarkpy')

# 因为app在post时不能准确地向webpy程序传递参数，这可能是一个bug, 为paste.fixture hack
def hackForInputs(f):
    def newInputs():
        if not web.ctx.has_key('env'):
            return {}
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

    # 需要用setUp来设置
    def setUp(self):
        self.appTestSetUp()
        app_errors.truncate(0)
        app.reset()

    def tearDown(self):
        self.appTestTearDown()
        error_msg = app_errors.getvalue()
        if error_msg:
            raise Exception(error_msg)

    # 向app程序发起一个GET请求
    def get(self, url, params={}, extra_environ = None):
        # 为webpy添加REQUEST_URI环境变量
        environ = {'REQUEST_URI': sh.paramsToUrl(url, params)}
        if extra_environ:
            environ.update(extra_environ)
        res = app.get(url, params, extra_environ=environ, expect_errors=True)
        return self._processResponse(res)

    # 向app程序发起一个POST请求
    def post(self, url, params={}, extra_environ = None):
        assert(isinstance(params, (dict, sh.storage_class)))
        # 为webpy添加REQUEST_URI环境变量
        environ = {'REQUEST_URI': url, 'CONTENT_TYPE': 'text/plain; charset=utf-8', }
        if extra_environ:
            environ.update(extra_environ)
        if not isinstance(params, sh.storage_class):
            params = sh.storage(params)
        # hack for use paste.fixture module test app.py
        environ['wsgi.input.zarkpy.post.hack'] = params
        res = app.post(url, params, extra_environ=environ, expect_errors=True)
        return self._processResponse(res)

    def _processResponse(self, res):
        if res.status == 200:
            return str(res.body)
        if res.status == 303:
            return ''
        else:
            print sh.printObject(res)
            raise Exception("Request Error %d" % res.status + res.errors)

    # 向app程序发起注册请求,并登录后返回Userid
    # 当不传入各项参数时就使用default_user中的默认值
    def register(self, email='', name='', password='', params={}, login=True):
        if email and not name:
            name = email # 自定义email时应该使用不同的name，因为name可能是unique key
        params['email'] = email if email else default_user['email']
        params['name'] = name if name else default_user['name']
        params['password'] = password if password else default_user['password']
        if not sh.model('User').getByEmail(params['email']):
            res = self.post('/api/user/register', params)
        if login:
            return self.login(params['email'], params['password'])
        else:
            return self.getUserid()

    # 向app程序发起登录请求，并返回登录用户的Userid
    def login(self, email='', password=''):
        params = {'action': 'login'}
        params['email'] = email if email else default_user['email']
        params['password'] = password if password else default_user['password']
        res = sh.loadsJson(self.post('/api/user/profile', params))
        assert res.is_login
        return res.id

    def logout(self):
        self.post('/api/user/profile', {'action':'logout'})

    def getLoginState(self):
        return sh.loadsJson(self.post('/api/user/profile', {'action':'isLogin'}))

    def getUserid(self):
        res = sh.loadsJson(self.post('/api/user/profile', {'action':'isLogin'}))
        return res.id if res.is_login else 0

    def insert(self, model_name, data, extra_environ={}):
        assert isinstance(model_name, (str, unicode))
        data['model_name'] = model_name
        return sh.loadsJson(self.post('/api/insert', data, extra_environ)).new_id

    def update(self, model_name, item_id, data, extra_environ={}):
        assert isinstance(model_name, (str, unicode))
        assert str(item_id).isdigit()
        data['model_name'] = model_name
        data['model_id'] = item_id
        return sh.loadsJson(self.post('/api/update', data, extra_environ)).affected

    def getItem(self, model_name, item_id):
        assert isinstance(model_name, (str, unicode))
        assert str(item_id).isdigit()
        item = sh.loadsJson(self.get('/api/get', {'model_name': model_name, 'model_id': item_id}))
        return ModelData(item, sh.model(model_name))

    # 使用当前用户id，模拟登录运行func
    def proxyDo(self, func, *params):
        curr_user_id = self.getUserid()
        assert curr_user_id, u'请先登录'
        return sh.proxyDo(curr_user_id, func, *params)

