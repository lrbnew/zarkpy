#coding=utf-8
import site_helper as sh
from Login import Login
# 当用户在第三方平台输入账号和密码后，先重定向到 Login.py ，如果需要用户手动注册，则导向这里
# 整个过程中，忽略用户的已登录状态
# ../../page/oauth/Register.html

class Register(Login):
    # User表的主键，为email或name
    PRIMARY_KEY = 'name'

    def GET(self):
        inputs = sh.inputs()
        assert inputs.get('access_token', '')
        assert inputs.get('state', '')
        return self._render(inputs.get('error', ''))

    def POST(self):
        inputs = sh.inputs()
        assert inputs.get('access_token', '')
        assert inputs.get('state', '')
        assert inputs.get(self.PRIMARY_KEY, '')
        assert inputs.get('password', '')
        site_name = inputs.state.partition('_')[0]
        user_model = sh.model('User')
        user_ctrl = sh.ctrl('User')
        oauth_model = sh.model('oauth.%sOAuth2' % site_name)
        oauth_ctrl  = sh.ctrl('oauth.%s' % site_name)
        cn_site_name = self._getCNSiteName()

        if self.PRIMARY_KEY == 'email':
            exists_user = user_model.getByEmail(inputs.email)
        elif self.PRIMARY_KEY == 'name':
            exists_user = user_model.getByName(inputs.name)

        # 如果primary_value没有注册过, 那么新建用户并绑定第三方帐号
        if not exists_user:
            inputs = oauth_ctrl.assignUserInfo(inputs, inputs.access_token)
            self.assignRegisterIP(inputs)
            conflict = user_ctrl.checkNewUser(inputs)
            if conflict:
                return self._render(conflict)

            new_id = user_model.insert(inputs)
            oauth_model.bindUseridByAccessToken(inputs.access_token, new_id)
            return self.login(new_id)

        # 否则已经注册过，检查密码是否正确
        else: 
            if self.PRIMARY_KEY == 'email':
                check_password = user_ctrl.validate(inputs.email, inputs.password)
            elif self.PRIMARY_KEY == 'name':
                check_password = user_ctrl.validateByName(inputs.name, inputs.password)

            if not check_password:
                error = '您已经注册过, 但您输入的密码不正确, 请重新输入'
                return self._render(error)

            oauth_model.bindUseridByAccessToken(inputs.access_token, exists_user.Userid)
            return self.login(exists_user.Userid)

    def _render(self, error_msg=''):
        inputs = sh.inputs()
        return sh.page.oauth.Register(inputs.access_token, inputs.state,
                self._getCNSiteName(), error_msg, inputs.get(self.PRIMARY_KEY))

    def _getCNSiteName(self):
        site_name = sh.inputs().state.partition('_')[0]
        return sh.ctrl('oauth.' + site_name).CN_SITE_NAME
