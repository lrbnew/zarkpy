#coding=utf-8
import site_helper as sh
import web

# ../../page/user/ResetPassword.html

class ResetPassword:

    def GET(self):
        inputs = web.input()
        if sh.session.is_login:
            return sh.page.user.ResetPassword()
        else:
            return sh.redirectToLogin()

    def POST(self):
        inputs = web.input()
        assert(6 <= len(inputs.new_password) < 60)
        user_model = sh.model('User')
        user_ctrl  = sh.ctrl('User')
        if not sh.session.is_login:
            return sh.redirectToLogin()

        Userid = sh.session.id
        user = user_model.get(Userid)
        assert(user is not None)

        if not user_ctrl.validate(user.email, inputs.old_password):
            return sh.page.user.ResetPassword('原密码输入错误, 请重新输入')

        user_model.update(Userid, dict(password=inputs.new_password))
        return sh.alert('重置密码成功')
