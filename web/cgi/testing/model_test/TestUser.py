#!coding=utf-8
import unittest
import site_helper as sh

db = sh.getDBHelper()
user_model = sh.model('User')
test_data = sh.storage(dict(email='sdjllyh@gmail.com', name='sdjl', password='123456', register_ip='127.0.0.1'))

class TestUser(unittest.TestCase):

    def setUp(self):
        db.executeQuery('delete from %s' % user_model.table_name)

    def test_getByEmail_getByName(self):
        id = user_model.insert(test_data)
        self.assertEqual(user_model.getByEmail(test_data.email).id, id)
        self.assertEqual(user_model.getByName(test_data.name).id, id)

    def test_getMD5Password(self):
        id = user_model.insert(test_data)
        item = user_model.get(id)
        # 保存的密码是经过getMD5Password函数加密后的
        self.assertEqual(user_model.getMD5Password(test_data.password), item.password)
        # 使用了sh.toMD5函数对密码加密，若修改了加密方式，请修改此测试
        self.assertEqual(item.password, sh.toMD5(test_data.password))

    # 必须输入email
    def test_decorater(self):
        decorator = sh.storage(dict(user_model.decorator))
        self.assertTrue(decorator.has_key('NotEmpty'))
        self.assertIn('email', decorator.NotEmpty['not_empty_attrs'])
