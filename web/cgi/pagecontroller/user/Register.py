#coding=utf-8
import web, re
import site_helper as sh
from pagecontroller import Insert

# ../../page/user/Register.html
# ../Insert.py

class Register(Insert):

    def GET(self):
        return sh.page.user.Register()

    def POST(self, inputs=None):
        if not inputs: inputs = self.getInputs()

        email = inputs.get('email', '')
        name = inputs.get('name', '').strip()
        password = inputs.get('password', '')
        assert(4 <= len(name) <=30)
        assert(6 <= len(password) < 60)

        if not re.match(r"^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$", email):
            return sh.page.user.Register('请输入正确的邮箱地址', email)

        inputs.register_ip = sh.session.ip

        model = sh.model('User')
        exists = model.getByEmail(email)
        if exists:
            return sh.page.user.Register('此邮箱已注册', email)

        new_id = model.insert(inputs)
        user = model.get(new_id)

        uc = sh.controller('User')
        uc.login(user, inputs.get('remember_me', 'no') == 'yes')

        if model.validation_request:
            uc.sendValidationEmail(user)
            return sh.alert('注册成功,请查收您的验证邮件')

        if sh.getReferer():
            return sh.redirect(sh.getReferer())
        else:
            return sh.alert('注册成功')
