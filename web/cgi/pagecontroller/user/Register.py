#coding=utf-8
# ../../page/user/Register.html
# ../../controller/User.py
# ../Insert.py
import site_helper as sh

class Register:

    def GET(self):
        return sh.page.user.Register()

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        uc = sh.ctrl('User')
        error = uc.checkNewUser(inputs)
        if error:
            return sh.page.user.Register(error, inputs.get('email', ''))

        new_id = uc.register(inputs)
        uc.loginById(new_id, inputs.get('remember_me', 'no') == 'yes')

        if sh.model('User').validation_request:
            uc.sendValidationEmail(user)
            return sh.alert('注册成功,请查收您的验证邮件')
        else:
            return sh.alert('注册成功')
