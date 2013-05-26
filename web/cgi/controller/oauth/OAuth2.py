#coding=utf-8
import site_helper as sh
# 用于保存第三方登录的数据
# 第三方平台提供的app id和secret key保存在SiteConfig中,比如oauth_appid_sina，oauth_appkey_sina
# 为了安全考虑不能明文发送secret key。发起https请求时，在参数中传递secret key是安全的

class OAuth2:
    # 第三方网站的名称
    SITE_NAME = ''
    CN_SITE_NAME = ''
    # 存储登录数据的model
    MODEL_NAME = ''
    # 要求第三方平台给与的权限
    SCOPE = ''
    # 引导用户去第三方平台登录的地址
    LOGIN_URL = ''
    # 获得access token的地址
    ACCESS_TOKEN_URL = ''
    # 获得access token的method，各个第三方网站的method不同
    ACCESS_TOKEN_METHOD = 'GET'
    # 获得uid的地址
    UID_URL = ''
    # 获得uid的method，各个第三方网站的method不同
    UID_METHOD = 'GET'
    # 分享内容到第三方平台的地址
    SHARE_URL = ''
    # 回调登录地址，用户在第三方平台输入账号和密码后第三方引导用户回调此地址
    REDIRECT_LOGIN = sh.config.HOST_NAME + '/oauth/login' 
    # 获得用户数据的地址
    USER_INFO_URL = ''

    # 利用state以防止csrf攻击(暂未实现此功能)
    def getState(self):
        return self.SITE_NAME

    # 从第三方返回的字符串中取出token和expires
    def pickAccessTokenAndExpires(self, content):
        res = sh.loadsJson(content)
        try:
            return res.access_token, res.expires_in
        except:
            raise Exception(content)

    # 从第三方返回的字符串中取出uid
    def pickUid(self, content):
        return sh.loadsJson(content).uid

    # 用第三方平台的用户数据赋值给data
    def assignUserInfo(self, data, access_token):
        return data

    # 创建登录第三方平台的url，访问此url即跳转到第三方平台输入账号和密码
    def createLoginUrl(self, state = None):
        return sh.joinUrl(self.LOGIN_URL, (
            'response_type', 'code', # 所有平台的response_type默认值均为code
            'client_id', self.getAppID(),
            'redirect_uri', self.REDIRECT_LOGIN,
            'scope', self.SCOPE,
            'state', state if state else self.getState(),
        ))

    # 创建获得access token的url。用户在第三方平台输入用户名和密码后第三方网站引导用户回调到本站，
    # 并附带authorization_code和state，本站用state区分是否为真实请求
    # 用authorization_code再去第三方平台获得access token
    def createAccessTokenUrl(self, authorization_code, state = None):
        return sh.joinUrl(self.ACCESS_TOKEN_URL, (
            'grant_type', 'authorization_code',
            'client_id', self.getAppID(),
            'client_secret',self.getAppKey(),
            'code', authorization_code,
            'state', state if state else self.getState(),
            'redirect_uri', self.REDIRECT_LOGIN,
        ))

    # 创建用access token获取Uid的url
    def createUidUrl(self, access_token):
        return sh.joinUrl(self.UID_URL, (
            'access_token', access_token,
        ))

    # 用access token去第三方平台读取uid
    def requestUidWithAccessToken(self, access_token):
        return str(self.pickUid(sh.requestHtmlContent(
            self.createUidUrl(access_token), method=self.UID_METHOD)))

    # 对将要发给第三方平台的数据进行签名，为了安全secret_key不应该被包含在data中
    def sign(self, data, secret_key):
        l = [sh.unicodeToStr('%s=%s' % (k,v)) for k,v in data.items()]
        l.sort()
        l.append(secret_key)
        md5 = hashlib.md5()
        md5.update(''.join(l))
        return md5.hexdigest()

    # 分享内容到第三方平台
    def share(self, *args):
        pass

    def getAppID(self):
        return sh.getSiteConfig('oauth2_appid_%s' % self.SITE_NAME.lower())

    def getAppKey(self):
        return sh.getSiteConfig('oauth2_appkey_%s' % self.SITE_NAME.lower())
