#!coding=utf-8
import unittest
import site_helper as sh

db = sh.getDBHelper()
test_image_path = '%sweb/cgi/testing/model_test/test_image.jpg' % sh.config.APP_ROOT_PATH
test_image_data = sh.storage(dict(filename=test_image_path, value=open(test_image_path).read(), imagetype='jpg'))

class TestOrderby(unittest.TestCase):

    def setUp(self):
        image_model = sh.model('Image')
        db.executeQuery('delete from %s' % image_model.table_name)

    # 指明all函数根据id逆序排序
    def test_all(self):
        # 插入两个数据
        decorator = [('Orderby', dict(orderby='{$primary_key} desc') ),]
        image_model = sh.model('Image', decorator)
        image_model.insert({image_model.image_key: test_image_data})
        image_model.insert({image_model.image_key: test_image_data})
        # 验证逆序
        items = image_model.all()
        self.assertGreater(items[0].id, items[1].id)
        # 可以通过显示指定orderby覆盖默认值
        items = image_model.all({'orderby': '{$primary_key}'})
        self.assertLess(items[0].id, items[1].id)
