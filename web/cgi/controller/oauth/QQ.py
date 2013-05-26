#coding=utf-8
from OAuth2 import OAuth2
import site_helper as sh

# OAuth2.py
''' help: http://wiki.opensns.qq.com '''

class QQ(OAuth2):
    SITE_NAME = 'QQ'
    CN_SITE_NAME = '腾讯QQ'
    MODEL_NAME = 'oauth.QQOAuth2'
    SCOPE = 'get_user_info,add_share,check_page_fans,add_t,add_pic_t,del_t,get_info'
    LOGIN_URL = 'https://graph.qq.com/oauth2.0/authorize'
    ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'
    ACCESS_TOKEN_METHOD = 'GET'
    UID_URL = 'https://graph.qq.com/oauth2.0/me'
    UID_METHOD = 'GET'
    SHARE_URL = 'https://graph.qq.com/share/add_share'
    USER_INFO_URL = 'https://graph.qq.com/user/get_user_info'

    def pickAccessTokenAndExpires(self, content):
        if 'access_token=' in content:
            access_token = content.partition('access_token=')[2].partition('&')[0]
            expires_in = content.partition('expires_in=')[2]
        else:
            access_token = ''
            expires_in = ''
        return access_token, expires_in

    def pickUid(self, content):
        return content.partition('"openid":"')[2].partition('"')[0]

    def assignUserInfo(self, data, access_token):
        new_data = sh.copy(data) if data else sh.storage()
        exists = sh.model(self.MODEL_NAME).getByAccessToken(access_token)
        if not exists: return new_data

        res =  sh.requestHtmlContent(self.USER_INFO_URL, (
            'access_token', access_token,
            'oauth_consumer_key', self.getAppID(),
            'openid', exists.uid,
            'format', 'json',
        ))

        if not res: return new_data
        res = sh.loadsJson(res)
        if res.ret != 0: return new_data

        if not new_data.has_key('name'):
            new_data['name'] = res.nickname

        if res.gender == '男':
            new_data['sex'] = '他'
        elif res.gender == '女':
            new_data['sex'] = '她'

        image_file = sh.requestImageFile(res.figureurl_2)
        if image_file:
            new_data['image_file'] = image_file

        return new_data

    def share(self, access_token, title):
        exists = sh.model(self.MODEL_NAME).getByAccessToken(access_token)
        if not exists: return None

        return sh.requestHtmlContent(self.SHARE_URL, (
            'access_token', access_token,
            'oauth_consumer_key', self.getAppID(),
            'openid', exists.uid,
            'title', title,
            'url', sh.config.HOST_NAME,
            'comment', None,
            'summary', None,
            'images', None,
            'source', 1,
        ))
