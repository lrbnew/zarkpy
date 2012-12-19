#coding=utf-8
import web
import site_helper as sh

# 根据cookie中的email和md5password自动登录,当用户选择remember_me时,login函数会设置这两个值
def loginByCookie(handler):
    if not sh.session.is_login:
        email = web.cookies().get('email', '')
        md5password = web.cookies().get('md5password', '')
        if email and md5password:
            user = sh.model('User').getOneByWhere('email=%s and password=%s', [email, md5password])
            if user:
                sh.controller('User').login(user)
    return handler()
