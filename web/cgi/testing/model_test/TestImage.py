#!coding=utf-8
import unittest
import os
import imghdr
import Image
import site_helper as sh

db = sh.getDBHelper()
image_model = sh.model('Image')

test_image_path = '%sweb/cgi/testing/model_test/test_image.jpg' % sh.config.APP_ROOT_PATH
assert os.path.exists(test_image_path), '用于测试的图片文件丢失了，可以随便用一张矩形jpg图代替'
test_image_data = sh.storage(dict(filename=test_image_path, value=open(test_image_path).read(), imagetype='jpg'))

class TestImage(unittest.TestCase):

    def setUp(self):
        db.executeQuery('delete from %s' % image_model.table_name)

    # 测试成功保存图片文件到sh.config.UPLOAD_IMAGE_PATH, 并可通过sh.config.UPLOAD_IMAGE_URL访问
    def test_insert_savesuccess(self):
        image_modle = sh.model('Image')
        image_model.use_convert = False # 不改变图片
        data = sh.storage({'data_name': 'User', 'data_id': 1, image_model.image_key: test_image_data})
        id = image_model.insert(data)
        item = image_model.get(id)
        # 访问路径以sh.config.UPLOAD_IMAGE_URL开头
        self.assertTrue(item.url.startswith(sh.config.UPLOAD_IMAGE_URL))
        image_path = sh.urlToPath(item.url)
        self.assertEqual(item.url, sh.pathToUrl(image_path)) # urlToPath和pathToUrl可互转
        # 用数据id命名, 并保持相同后缀
        self.assertTrue(image_path.endswith('/%d.%s' % (id, test_image_data.imagetype)))
        # 保存的文件数据与测试数据一致
        self.assertTrue(os.path.exists(image_path))
        self.assertEqual(open(image_path).read(), test_image_data.value)

    # update时忽略图片数据
    def test_update(self):
        image_modle = sh.model('Image')
        image_model.use_convert = False # 不改变图片
        data = sh.storage({'data_name': 'User', 'data_id': 1, image_model.image_key: test_image_data})
        id = image_model.insert(data)
        item = image_model.get(id)
        # 更新图片数据
        image_model.update(id, {'image_file': {'filename':'new', 'value':'new', 'imagetype':'png'}, 'data_id': 2})
        item2 = image_model.get(id)
        # 其它数据更新成功
        self.assertEqual(item2.data_id, 2)
        # url不变
        self.assertEqual(item.url, item2.url)
        # 图片数据不变
        image_path = image_modle.getFilePath(id)
        self.assertEqual(open(image_path).read(), test_image_data.value)

    # 测试转换，压缩尺寸
    def test_insert_convert(self):
        image_modle = sh.model('Image')
        image_model.use_convert = True # 改变图片
        image_model.convert_type = 'png'
        image_model.max_width = 50
        image_model.max_height = 60
        data = sh.storage({'data_name': 'User', 'data_id': 1, image_model.image_key: test_image_data})
        id = image_model.insert(data)
        item = image_model.get(id)
        image_path = sh.urlToPath(item.url)
        # 转换为png格式
        self.assertTrue(image_path.endswith('/%d.png' % (id)))
        self.assertEqual(imghdr.what(None, open(image_path).read()), 'png')
        # 压缩为50x50. 因为会保持原有比例，所以压缩后高度依然是50, 不是60
        self.assertEqual(Image.open(image_path).size, (50, 50))

        # 当max_height与max_width有其中之一为None时就不压缩
        image_model.max_height = None
        id2 = image_model.insert(data)
        item2 = image_model.get(id2)
        # 虽然不压缩尺寸，但是要转换格式
        image_path = sh.urlToPath(item2.url)
        self.assertTrue(image_path.endswith('/%d.png' % (id2)))
        # 依然是原来的尺寸
        self.assertEqual(Image.open(image_path).size, Image.open(test_image_data.filename).size)

    # 可以通过__ignore_convert_image显示声明不转换图片
    def test_ignore_convert_image(self):
        image_modle = sh.model('Image')
        image_model.use_convert = True
        image_model.convert_type = 'png'
        image_model.max_width  = 50
        image_model.max_height = 60
        data = sh.storage({'data_name': 'User', 'data_id': 1, image_model.image_key: test_image_data})
        data['__ignore_convert_image'] = True
        id = image_model.insert(data)
        item = image_model.get(id)
        image_path = sh.urlToPath(item.url)
        # 保存的文件数据与测试数据一致, 文件没有被convert
        self.assertEqual(open(image_path).read(), test_image_data.value)

    def test_getUrl_getFilePath(self):
        image_modle = sh.model('Image')
        image_model.use_convert = False
        data = sh.storage({'data_name': 'User', 'data_id': 1, image_model.image_key: test_image_data})
        id = image_model.insert(data)
        item = image_model.get(id)
        self.assertEqual(item.url, image_model.getUrl(id))
        self.assertEqual(sh.urlToPath(item.url), image_model.getFilePath(id))
