#coding=utf-8
from OAuth2 import OAuth2
import site_helper as sh

# OAuth2.py
''' help: http://open.weibo.com/wiki/API%E6%96%87%E6%A1%A3_V2 '''

class Sina(OAuth2):
    SITE_NAME = 'Sina'
    CN_SITE_NAME = '新浪微博'
    MODEL_NAME = 'oauth.SinaOAuth2'
    SCOPE = '' # 新浪不使用SCOPE
    LOGIN_URL = 'https://api.weibo.com/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://api.weibo.com/oauth2/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    UID_URL = 'https://api.weibo.com/oauth2/get_token_info'
    UID_METHOD = 'POST'
    SHARE_URL = 'https://api.weibo.com/2/statuses/update.json'
    USER_INFO_URL = 'https://api.weibo.com/2/users/show.json'
    FRIEND_UIDS = 'https://api.weibo.com/2/friendships/friends/ids.json'
    
    def assignUserInfo(self, data, access_token):
        new_data = sh.copy(data) if data else sh.storage()
        exists = sh.model(self.MODEL_NAME).getByAccessToken(access_token)
        if not exists: return new_data

        res =  sh.requestHtmlContent(self.USER_INFO_URL, (
            'access_token', access_token,
            'oauth_consumer_key', self.getAppID(),
            'uid', exists.uid,
        ))

        if not res: return new_data

        res = sh.loadsJson(res)

        if res.get('error_code', None): return new_data

        if not new_data.has_key('name'):
            new_data['name'] = res.screen_name

        if res.gender == 'm':
            new_data['sex'] = '他'
        elif res.gender == 'f':
            new_data['sex'] = '她'
        else:
            new_data['sex'] = '保密'

        image_file = sh.requestImageFile(res.avatar_large)
        if image_file:
            new_data['image_file'] = image_file

        return new_data

    def share(self, access_token, comment):
        exists = sh.model(self.MODEL_NAME).getByAccessToken(access_token)
        if not exists: return None

        return sh.requestHtmlContent(self.SHARE_URL, {
            'access_token': access_token,
            'oauth_consumer_key': self.getAppID(),
            'uid': exists.uid,
            'status': comment,
        }, 'POST')

    def getFollowUids(self, access_token, uid):
        res = sh.requestHtmlContent(self.FRIEND_UIDS, {
            'access_token': access_token,
            'uid': uid,
            'count': 5000
        })
        if not res: return []
        res = sh.loadsJson(res)
        if res.get('error_code', None): return []

        return res.ids
