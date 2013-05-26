#coding=utf-8
from .. import Model
import datetime
''' 保存用户使用第三方账号登录的状况，各字段的含义:
    Userid: 与本系统绑定的用户id
    uid: 第三方平台提供的唯一用户id，不同的APPKEY拿到的uid是不一样的
    access_token: 第三方平台提供的认证标识，有效期过后需要重新获得，每个平台的有效期是不一样的
    access_expires: access_token的有效期，一个单位秒的整数
    refesh_time: 获得access_token的时间，与access_expires可计算出access_token是否过期
    allow_share: 用户是否允许本站自动在第三方平台分享内容
'''

class OAuth2(Model):
    table_name = ''
    column_names = ['Userid','uid','access_token','access_expires','refesh_time','allow_share',]
    decorator = [
        ('NotEmpty', dict(not_empty_attrs=['uid', 'access_token', 'access_expires']) ),
    ]

    # 插入数据时，删除access_token重复的老数据
    def insert(self, data):
        del_query = 'delete from {$table_name} where access_token=%s'
        self.db.delete(self.replaceAttr(del_query), [data['access_token']])
        return Model.insert(self, data)

    def getByUid(self, uid):
        return self.getOneByWhere('uid=%s', [uid])

    def getByAccessToken(self, access_token):
        return self.getOneByWhere('access_token=%s', [access_token])

    # 更新uid的token及其有效期
    def refreshToken(self, uid, access_token, access_expires):
        exists = self.getByUid(uid)
        if not exists: return 0
        return self.update(exists.id, dict(access_token=access_token,
                access_expires=access_expires, refesh_time=datetime.datetime.now()))

    def bindUseridByAccessToken(self, access_token, Userid):
        exists = self.getByAccessToken(access_token)
        if exists:
            self.update(exists.id, dict(Userid=Userid))

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id       int unsigned not null auto_increment,
            Userid                int unsigned not null default 0,
            uid                   varchar(100) not null,
            access_token          varchar(100) not null,
            access_expires        int unsigned not null default 0,
            refesh_time           timestamp not null default current_timestamp,
            allow_share           enum('yes','no') not null default 'yes',
            primary key           ({$table_name}id),
            unique key            (access_token),
            unique key            (uid),
            key                   (Userid)
        )ENGINE=InnoDB; '''
