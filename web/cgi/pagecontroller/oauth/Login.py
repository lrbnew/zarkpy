#coding=utf-8
import random
import site_helper as sh
# 用户在第三方平台输入密码后返回到此login, 并提供code(authorization_code)，本站在用code获得access_token
# 获得access_token后，如果还没有注册则引导用户注册或自动注册，若已注册则直接登录
# 整个过程中，忽略用户的已登录状态

class Login:
    # 如果用户没有注册，则如何处理？有to_register和auto_register可选
    # auto_register仅在使用唯一用户名登录时可用，因为assignUserInfo函数拿不到邮箱
    NO_REGISTER_ACTION = 'auto_register'
    # 是否自动记住我
    REMEMBER_ME = False
    # 仅返回测试api登录的连接？
    TEST_API_LOGIN = True

    def GET(self):
        inputs = sh.inputs()
        assert(inputs.has_key('code'))
        assert(inputs.has_key('state'))

        site_name = inputs.state.partition('_')[0]
        authorization_code = inputs.code.strip()
        oauth_ctrl  = sh.ctrl('oauth.%s' % site_name)
        oauth_model = sh.model('oauth.%sOAuth2' % site_name)
        user_ctrl  = sh.ctrl('User')
        user_model = sh.model('User')

        token_url = oauth_ctrl.createAccessTokenUrl(authorization_code)
        content =  sh.requestHtmlContent(token_url, None, oauth_ctrl.ACCESS_TOKEN_METHOD)
        assert content, u'第三方返回的数据有误'

        access_token, access_expires = oauth_ctrl.pickAccessTokenAndExpires(content)
        requested_uid = oauth_ctrl.requestUidWithAccessToken(access_token)
        assert requested_uid, u'第三方返回的数据有误'
        if self.TEST_API_LOGIN:
            login_url = '%s/api/oauth/login?access_token=%s&access_expires=%s&uid=%s&state=%s' % (sh.config.HOST_NAME, access_token, access_expires, requested_uid, inputs.state)
            return '<a href="%s" >%s</a>' % (login_url, login_url)

        # 因为access_token是动态变化的，所以要用requested_uid来判断是否登录过
        # 这也避免了access_token变化时插入重复的uid
        exists = oauth_model.getByUid(requested_uid)

        # 如果当前uid还没有插入数据库，则先插入再考虑绑定Userid
        if not exists:
            new_oauth_id = oauth_model.insert(dict(uid = requested_uid,
                access_token = access_token, access_expires = access_expires))
            exists = oauth_model.get(new_oauth_id)

        # 如果已绑定Userid则登录
        if exists.Userid:
            return self.login(exists.Userid)

        # 如果希望自动注册，则注册并绑定后登录
        if self.NO_REGISTER_ACTION == 'auto_register':
            data = oauth_ctrl.assignUserInfo(sh.storage(), access_token)
            self.assignRandomPassword(data)
            self.assignRegisterIP(data)
            conflict = user_ctrl.checkNewUser(data)
            if conflict:
                return self.redirectToRegister(access_token, inputs.state, error=conflict)

            new_user_id = user_model.insert(data)
            oauth_model.update(exists.id, dict(Userid=new_user_id))
            return self.login(new_user_id)
        # 否则希望用户自己注册
        elif self.NO_REGISTER_ACTION == 'to_register':
            return self.redirectToRegister(access_token, inputs.state)

    def redirectToRegister(self, access_token, state, error=''):
        return sh.redirect('/oauth/register?access_token=%s&state=%s&error=%s' % (access_token, state, sh.quote(error)))

    def login(self, Userid):
        exists_user = sh.model('User').get(Userid)
        assert exists_user, u'用户不存在'
        sh.ctrl('User').login(exists_user, self.REMEMBER_ME)
        return sh.redirect('/')

    # 为注册用户设置32位的随机密码
    def assignRandomPassword(self, data):
        if not data.has_key('password'):
            data['password'] = str(random.randint(10000000000000000000000000000000,
                    100000000000000000000000000000000))

    # 设置用户的注册IP
    def assignRegisterIP(self, data):
        data['register_ip'] = sh.session.ip
