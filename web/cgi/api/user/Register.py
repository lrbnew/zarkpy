#coding=utf-8
import re
import site_helper as sh

# ../../controller/User.py

class Register:

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        uc = sh.ctrl('User')
        error = uc.checkNewUser(inputs)
        if error:
            return sh.toJsonp({'is_login': False, 'error': error})

        new_id = uc.register(inputs)
        uc.loginById(new_id, inputs.get('remember_me', 'no') == 'yes')

        if sh.model('User').validation_request:
            uc.sendValidationEmail(user)
            return sh.toJsonp({'is_login': True, 'id': new_id, 'msg': '注册成功,请查收您的验证邮件'})
        else:
            return sh.toJsonp({'is_login': True, 'id': new_id, 'msg': '注册成功'})
