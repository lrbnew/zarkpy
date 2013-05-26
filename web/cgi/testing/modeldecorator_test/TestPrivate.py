#coding=utf-8
# ../../modeldecorator/Private.py
import site_helper as sh
from .. import AppTest

db = sh.getDBHelper()
test_model_name = 'ForTestPrivate'

class TestPrivate(AppTest.AppTest):

    def appTestSetUp(self):
        db.executeQuery('delete from %s' % sh.model(test_model_name).table_name)
        db.executeQuery('delete from %s' % sh.model('Private').table_name)

    def appTestTearDown(self):
        self.logout()

    def test_insert(self):
        self.register()
        my_id = self.getUserid()
        model = sh.model(test_model_name)
        pri_model = sh.model('Private')
        # 插入一个数据
        pri_1 = pri_model.getNextPrivateid(test_model_name, my_id)
        new_id = self.insert(test_model_name, dict(title='test'))
        # 新数据的id等于刚才得到的next private id
        self.assertEqual(pri_1, new_id)
        # Private表中的next private id增1
        pri_2 = pri_model.getNextPrivateid(test_model_name, my_id)
        self.assertEqual(pri_1+1, pri_2)
        # 插入数据会自动记录private id
        item = self.getItem(test_model_name, new_id)
        self.assertEqual(item.private_id, pri_1)
        # 因为self.getItem是客户端，拿不到Private包装过的item
        # 所以主键依然是ForTestPrivateid, 而这个主键在正式中应该是private_id
        self.assertEqual(item._primary_key, 'ForTestPrivateid')

    # 模拟多个用户操作
    # 同时测试以下函数: delete all getCount update getOneByWhere
    def test_insert_multi_user(self):
        # 登录user1插入一些数据
        self.register('user1@sparker5.com')
        model = sh.model(test_model_name)
        new_id = self.proxyDo(model.insert, dict(title='a1'))
        new_id = self.proxyDo(model.insert, dict(title='a2'))
        item_a1 = self.proxyDo(model.get, new_id)

        # 登录user2插入一些数据
        self.register('user2@sparker5.com')
        new_id = self.proxyDo(model.insert, dict(title='b1'))
        new_id = self.proxyDo(model.insert, dict(title='b2'))

        # 登录user1, 再次插入一个数据
        self.login('user1@sparker5.com')
        new_id = self.proxyDo(model.insert, dict(title='a3'))
        # user1插入的数据的id是连贯的(不会受到其他用户的影响)
        item_a2 = self.proxyDo(model.get, new_id)
        self.assertEqual(item_a1.id + 1, item_a2.id)
        # getCount不包含user2的数据
        self.assertEqual(self.proxyDo(model.getCount), 3)
        # 通过item.id更新数据, 效果等同于使用new_id
        self.proxyDo(model.update, item_a2.id, dict(title='a3`'))
        self.assertEqual(self.proxyDo(model.get, new_id).title, 'a3`')
        # 使用getOneByWhere不需要显示指出Userid
        curr_user_id = self.getUserid()
        item_a3 = sh.proxyDo(curr_user_id, model.getOneByWhere, 'title=%s', ['a3`'])
        self.assertEqual(item_a3.id, new_id)

        # 用id删除user1的所有数据
        for i in self.proxyDo(model.all):
            self.proxyDo(model.delete, i.id)
        self.assertEqual(len(self.proxyDo(model.all)), 0)

        # 登录user2, 所有数据均在
        self.login('user2@sparker5.com')
        self.assertEqual(len(self.proxyDo(model.all)), 2)

    def test_get(self):
        self.register()
        model = sh.model(test_model_name)
        new_id = self.proxyDo(model.insert, dict(title='test'))
        # 假装用户拿到item
        item = self.proxyDo(model.get, new_id)
        # 返回数据的主键应该是private_id
        self.assertEqual(item._primary_key, 'private_id')
        self.assertEqual(item.id, item.private_id)

    def test_replaceInsert(self):
        self.register()
        model = sh.model(test_model_name)

        new_id_1 = self.proxyDo(model.insert, dict(title='test'))
        item_1 = self.proxyDo(model.get, new_id_1)

        new_id_2 = self.proxyDo(model.replaceInsert, dict(title='test'))
        item_2 = self.proxyDo(model.get, new_id_2)
        
        self.assertEqual(new_id_1+1, new_id_2)
        # replaceInsert插入，private_id也会增加
        self.assertEqual(item_1.private_id + 1, item_2.private_id)
        # 老数据被删除
        self.assertIsNone(self.proxyDo(model.get, new_id_1))

    # 显示禁用private功能
    def test_unuse_private(self):
        model = sh.model(test_model_name)
        insert_query = 'insert into ' + test_model_name+ ' (Userid, private_id, title) values (%s, %s, %s)'
        db.insert(insert_query, [1, 1, 'a'])
        db.insert(insert_query, [2, 1, 'b'])
        db.insert(insert_query, [3, 1, 'c'])
        items = model.all(dict(use_private=False))
        self.assertEqual(len(items), 3)
        
# 用于测试Private的类
from model import Model
class ForTestPrivate(Model):
    table_name      = 'ForTestPrivate'
    column_names    = ['Userid','private_id','title',]
    test_decorator  = [
        ('Private', dict(user_id_key='Userid', primary_key='private_id', use_private=True) ),
    ]
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Userid      int unsigned not null default 0,
            private_id  int unsigned not null default 0,
            title       varchar(100)  charset utf8 not null default '',
            primary key ({$table_name}id),
            unique key (title)
        )ENGINE=InnoDB; '''

from .. import registerModel
registerModel(ForTestPrivate)
