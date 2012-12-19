#coding=utf-8
import web
import site_helper as sh

# ../../page/user/Login.html

class Login:

    def GET(self):
        action = sh.getEnv('REQUEST_URI').strip('/')
        if action == 'login':
            return sh.page.user.Login()
        if action == 'logout':
            sh.controller('User').logout()
            return sh.redirect('/')

    def POST(self, inputs=None):
        if not inputs: inputs = web.input()
        assert(inputs.get('email', '').strip())
        assert(inputs.get('password', ''))

        uc = sh.controller('User')
        model = sh.model('User')
        action = sh.getEnv('REQUEST_URI').strip('/')

        if action == 'login':
            if not uc.validate(inputs.email, inputs.password):
                return sh.page.user.Login('您输入的用户名或密码不对, 请重新输入', inputs.email)

            user = model.getByEmail(inputs.email)

            if user.dead == 'yes':
                return sh.alert('登录失败,你已被列入黑名单,请联系管理员')

            uc.login(user, inputs.get('remember_me', '') == 'on')

            if sh.getReferer():
                return sh.redirect(sh.getReferer())
            else:
                return sh.alert('登录成功. 欢迎回来!')
