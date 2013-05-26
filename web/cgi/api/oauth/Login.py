#coding=utf-8
from pagecontroller.oauth import Login as pLogin
import site_helper as sh
# 此api类似 ../../pagecontroller/oauth/Login.py 但是略去了向服务器端获得access_token的过程
# 客户端app自己引导用户获得access_token和uid，然后再向此api发起登录请求
# 此api会先用access_token去第三方平台核对uid是否正确
# 然后用inputs中的数据尝试注册，因此此api同时也是register的api
# 当is_login=False时，客户端app自己引导用户修改注册信息，然后再向此api发起请求

class Login(pLogin):
    REMEMBER_ME = False

    def GET(self):
        return self.POST()

    def POST(self):
        inputs = sh.inputs()
        assert inputs.get('access_token', '')
        assert inputs.get('access_expires', '')
        assert inputs.get('uid', '')
        assert inputs.get('state', '')

        site_name = inputs.state.partition('_')[0]
        oauth_ctrl  = sh.ctrl('oauth.%s' % site_name)
        oauth_model = sh.model('oauth.%sOAuth2' % site_name)
        user_ctrl  = sh.ctrl('User')
        user_model = sh.model('User')

        requested_uid = oauth_ctrl.requestUidWithAccessToken(inputs.access_token)
        # 如果access_token和uid验证不对，则不让登录
        if not requested_uid or requested_uid != inputs.uid:
            return sh.toJsonp(dict(error = "该第三方帐号未绑定任何站内帐号", is_login = False))

        exists = oauth_model.getByUid(requested_uid)

        # 如果当前uid还没有插入数据库，则先插入再考虑绑定Userid
        if not exists:
            new_id = oauth_model.insert(dict(uid = requested_uid,
                access_token = inputs.access_token, access_expires = inputs.access_expires))
            exists = oauth_model.get(new_id)

        if exists.Userid: # 如果已绑定本站帐号
            return self.login(exists.Userid)

        inputs = oauth_ctrl.assignUserInfo(inputs, inputs.access_token)
        self.assignRandomPassword(inputs)
        self.assignRegisterIP(inputs)
        conflict = user_ctrl.checkNewUser(inputs)
        if conflict:
            return sh.toJsonp(dict(is_login = False, error = conflict,
                name = inputs.get('name', ''), sex = inputs.get('sex', '')))

        new_id = user_model.insert(inputs)
        oauth_model.update(exists.id, dict(Userid=new_id))

        return self.login(new_id)

    def login(self, Userid):
        exists_user = sh.model('User').get(Userid)
        assert exists_user, u'用户不存在'
        sh.ctrl('User').login(exists_user, self.REMEMBER_ME)
        return sh.toJsonp(dict(is_login = True, Userid = Userid, name = sh.session.name))

