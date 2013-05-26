#coding=utf-8
from OAuth2 import OAuth2
import site_helper as sh

# OAuth2.py
''' help: http://wiki.dev.renren.com/wiki/Web%E7%BD%91%E7%AB%99%E6%8E%A5%E5%85%A5 '''

class RenRen(OAuth2):
    SITE_NAME = 'RenRen'
    CN_SITE_NAME = '人人网'
    MODEL_NAME = 'oauth.RenRenOAuth2'
    SCOPE = 'publish_share publish_feed publish_comment'
    LOGIN_URL = 'https://graph.renren.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://graph.renren.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    UID_URL = 'http://api.renren.com/restserver.do'
    UID_METHOD = 'GET'
    SHARE_URL = '' # 人人不使用此值
    USER_INFO_URL = '' # 人人不使用此值

    # 人人要求发起请求时提供额外信息和签名
    def _request(self, params):
        params = sh.copy(params)
        params['v'] = '1.0'
        params['format'] = 'JSON'
        params['sig'] = self.sign(params, self.getAppKey())
        return sh.requestHtmlContent(self.UID_URL, params, 'POST')

    def requestUidWithAccessToken(self, access_token):
        params = {
            'method':   'users.getLoggedInUser',
            'access_token':   access_token,
        }
        res = self._request(params)
        return self.pickUid(res) if res else None

    def assignUserInfo(self, data, access_token):
        new_data = sh.copy(data) if data else sh.storage()
        params = {
            'method':   'users.getInfo',
            'access_token':   access_token,
            'fields': 'name,sex,mainurl',
        }
        content = sh.loadsJson(self._request(params).partition('[')[2].rpartition(']')[0])

        if not new_data.has_key('name'):
            new_data['username'] = content.name

        if str(content.sex) == '1':
            new_data['sex'] = '他'
        elif str(content.sex) == '2':
            new_data['sex'] = '她'

        image_file = sh.requestImageFile(content.mainurl)
        if image_file:
            new_data['image_file'] = image_file

        return new_data

    def share(self, access_token, comment):
        params = {
            'method':   'share.share',
            'type':     6,
            'comment':  comment,
            'access_token':  access_token,
            'url':  sh.config.HOST_NAME,
        }
        return self._request(params)
