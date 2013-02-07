#!coding=utf-8
import site_helper as sh
from .. import AppTest
AppTest = AppTest.AppTest
from model import Model

class TestRecordRequestInfo(AppTest):

    def test_insert_and_update(self):
        # 注册，insert数据必须先登录
        self.register()
        # 设置环境变量
        extra_environ = {'HTTP_USER_AGENT': 'firefox', 'HTTP_REFERER': 'http://sparker5.com'}
        # 插入数据
        data = dict(title='hi', model_name='ForTestRecordRequestInfo')
        self.post('/cgi/insert', data, extra_environ)
        model = sh.model('ForTestRecordRequestInfo')
        item = model.get(1)
        # 验证RecordRequestInfo自动记录了环境变量的值
        self.assertEqual(item.user_agent, 'firefox')
        self.assertEqual(item.referer, 'http://sparker5.com')
        # 修改环境变量然后update
        extra_environ['HTTP_USER_AGENT'] = 'chrome'
        data['model_id'] = 1
        self.post('/cgi/update', data, extra_environ)
        # update时会修改记录值
        item = model.get(1)
        self.assertEqual(item.user_agent, 'chrome')
        self.assertEqual(item.referer, 'http://sparker5.com')


# 用于测试RecordRequestInfo的类
class ForTestRecordRequestInfo(Model):
    table_name      = 'ForTestRecordRequestInfo'
    column_names    = ['Userid', 'title', 'user_agent', 'referer', 'ip']
    test_decorator  = [
        ('RecordRequestInfo', dict(ip='ip', user_agent='HTTP_USER_AGENT', referer='HTTP_REFERER') ),
    ]
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Userid          int unsigned  not null default 0,
            title           varchar(100) not null default '',
            user_agent      varchar(100) not null default '',
            referer         varchar(100) not null default '',
            ip              char(15) not null default '',
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''

from .. import registerModel
registerModel(ForTestRecordRequestInfo)
