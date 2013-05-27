#coding=utf-8
import site_helper as sh

# 验证用户邮箱，因为code只发给了注册用户的邮箱，所以只要exists就认为邮箱正确
# ../../model/UserValidation.py

class Validate:

    def GET(self):
        inputs = sh.inputs()
        assert(inputs.has_key('Userid'))
        assert(inputs.has_key('code'))

        model = sh.model('UserValidation')
        exists = model.getOneByWhere('Userid=%s and code=%s', inputs.Userid, inputs.code)

        if exists:
            sh.model('User').update(inputs.Userid, dict(activated='yes'))
            model.delete(exists.id)
            return sh.alert('验证邮箱成功')
        else:
            return sh.redirectTo404()
