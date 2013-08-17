#coding=utf-8
# ../../page/user/ForgetPassword.html
from datetime import datetime
import web
import site_helper as sh

class ForgetPassword:

    def GET(self):
        inputs = web.input()
        return sh.page.user.ForgetPassword(inputs.get('Userid', None), inputs.get('code', ''))

    def POST(self):
        inputs = web.input()
        if inputs.action == 'send_code':
            user = sh.model('User').getByEmail(inputs.email.strip())
            if user:
                sh.ctrl('User').sendForgetPasswordEmail(user)
            return sh.alert('发送成功,请查收您的邮件(可能在"垃圾邮件"中)。', '/')

        elif inputs.action == 'reset_password':
            assert(6 <= len(inputs.password) < 60)
            user_model = sh.model('User')
            code_model = sh.model('UserForgetPassword')
            exists = code_model.getOneByWhere('Userid=%s and code=%s', inputs.Userid, inputs.code)
            if not exists:
                return sh.alert('链接无效,请重新申请')
            if (datetime.now() - exists.created).seconds > code_model.expires:
                return sh.alert('链接已过期,请重新申请')
            user_model.update(inputs.Userid, dict(password=inputs.password))
            code_model.delete(exists.id)
            return sh.alert('重设密码成功,请登录', '/login')
