#coding=utf-8
import unittest
import site_helper as sh

db = sh.getDBHelper()
image_model = sh.model('Image')

test_user_data = dict(email='sdjllyh@gmail.com', name='sdjl', password='123456', register_ip='127.0.0.1')
test_image_path = '%sweb/cgi/testing/model_test/test_image.jpg' % sh.config.APP_ROOT_PATH
test_image_data = sh.storage(dict(filename=test_image_path, value=open(test_image_path).read(), imagetype='jpg'))

class TestCascade(unittest.TestCase):

    def setUp(self):
        user_model = sh.model('User')
        db.executeQuery('delete from %s' % user_model.table_name)
        db.executeQuery('delete from %s' % image_model.table_name)

    # 测试级联递增
    # 每插入一个User, 同时对data中Imageid指定的Image数据的data_id加1
    # 只是为了测试,这种用法并不符合Image的设计
    def test_insert(self):
        decorator = [('Cascade', dict(
            increase=[('Image', 'data_id'), ],
        ))]
        # 插入一张图片
        image_data = {image_model.image_key: test_image_data, 'data_id': 1}
        id1 = image_model.insert(image_data)
        # 对插入的user数据关联Imageid
        user_data = sh.copy(test_user_data)
        user_data['Imageid'] = id1
        user_model = sh.model('User', decorator)
        # 插入user数据
        user_model.insert(user_data)
        # 被关联的图片data_id增加了1
        item = image_model.get(id1)
        self.assertEqual(item.data_id, 2)

    # 测试级联递减
    # 每删除一个User, 同时对被删除数据的Imageid关联的Image的data_id减1
    def test_delete_decrease(self):
        decorator = [('Cascade', dict(
            decrease=[('Image', 'data_id'), ],
        ))]
        # 插入一张图片
        image_data = {image_model.image_key: test_image_data, 'data_id': 1}
        id1 = image_model.insert(image_data)
        # 插入一个user
        user_data = sh.copy(test_user_data)
        user_data['Imageid'] = id1
        id2 = sh.model('User').insert(user_data)
        # data_id不变
        item1 = image_model.get(id1)
        self.assertEqual(item1.data_id, 1)
        # 删除user
        user_model = sh.model('User', decorator)
        user_model.delete(id2)
        # 被关联的图片data_id减少了1
        item2 = image_model.get(id1)
        self.assertEqual(item2.data_id, 0)

    # 测试级联删除
    # 每删除一个User, 同时删除Image中data_id等于Userid的数据
    def test_delete_delete(self):
        decorator = [('Cascade', dict(
            delete=[('Image', 'data_id'), ],
        ))]
        # 插入一个user
        id1 = sh.model('User').insert(test_user_data)
        # 插入一张图片, 并关联data_id为Userid
        image_data = {image_model.image_key: test_image_data, 'data_id': id1}
        id2 = image_model.insert(image_data)
        id3 = image_model.insert(image_data)
        # 删除user
        user_model = sh.model('User', decorator)
        user_model.delete(id1)
        # 图片数据也被删除
        self.assertIsNone(image_model.get(id2))
        self.assertIsNone(image_model.get(id3))
