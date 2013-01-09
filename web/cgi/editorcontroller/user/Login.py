#coding=utf-8
import web
import site_helper as sh

# ../../editor/user/Login.html
# ../../controller/AdminUser.py

class Login:

    def GET(self):
        action = sh.getEnv('REQUEST_URI').partition('?')[0].strip('/')
        if action == 'admin/login':
            return sh.editor.user.Login()
        if action == 'admin/logout':
            sh.ctrl('AdminUser').logout()
            return sh.redirect('/')

    def POST(self, inputs=None):
        if not inputs: inputs = web.input()
        assert(inputs.get('email', '').strip())
        assert(inputs.get('password', ''))

        uc = sh.ctrl('AdminUser')
        model = sh.model('AdminUser')
        action = sh.getEnv('REQUEST_URI').partition('?')[0].strip('/')

        if action == 'admin/login':
            if not uc.validate(inputs.email, inputs.password):
                return sh.editor.user.Login('密码不对', inputs.email)
            user = model.getByEmail(inputs.email)
            uc.login(user)
            return sh.redirect('/admin')
