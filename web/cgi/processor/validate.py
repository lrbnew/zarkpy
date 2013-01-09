#coding=utf-8
import site_helper as sh

OPEN_URL = ['/login', '/register', '/api/user-image']
REQUIRE_LOGIN_URL = ['/insert', '/update', '/delete', '/accounts']

# 对访问进行权限验证
# 注意，不要对"将来的请求"做出限制，比如限制非注册用户访问所有的POST请求
# 因为提前限制"将来可能会增加的请求"会导致程序逻辑变得更不"透明"
# 这会导致此模块与将来的模块之间不"正交"
def validate(handler):
    request_path = sh.getEnv('REQUEST_URI').partition('?')[0]

    is_login = sh.session.get('is_login', False)
    is_admin = sh.session.get('is_admin', False)
    method   = sh.getEnv('REQUEST_METHOD')

    # 禁止未登录用户访问REQUIRE_LOGIN_URL中的地址
    if not is_login and request_path in REQUIRE_LOGIN_URL:
        return sh.redirectToLogin()

    # 禁止非admin用户访问admin页面
    if not is_admin and request_path.startswith('/admin') and request_path != '/admin/login':
        return sh.redirect('/admin/login')

    return handler()
