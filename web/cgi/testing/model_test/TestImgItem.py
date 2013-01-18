#!coding=utf-8
import unittest
import os
import imghdr
import Image
import site_helper as sh

''' 因为ImgItem.table_name为空，所以没有具体的表，这里使用ImgItem的子类User代替
    如果你打算修改User的基类，请找一个table_name不为空的ImgItem子类替换User
    并修改test_data '''

db = sh.getDBHelper()
imgitem_model = sh.model('User')
image_model = sh.model('Image')

test_data = dict(email='sdjllyh@gmail.com', name='sdjl', password='123456', register_ip='127.0.0.1')
test_image_path = '%sweb/cgi/testing/model_test/test_image.jpg' % sh.config.APP_ROOT_PATH
test_image_data = sh.storage(dict(filename=test_image_path, value=open(test_image_path).read(), imagetype='jpg'))

class TestImgItem(unittest.TestCase):

    def setUp(self):
        db.executeQuery('delete from %s' % imgitem_model.table_name)
        db.executeQuery('delete from %s' % image_model.table_name)

    # 测试成功用Image保存图片, 并关联Imageid
    def test_insert(self):
        imgitem_model.use_convert = True
        imgitem_model.convert_type = 'png'
        imgitem_model.max_width = 50
        imgitem_model.max_height = 60

        data = sh.copy(test_data)
        data[image_model.image_key] = test_image_data
        old_count = len(image_model.all())
        id = imgitem_model.insert(data)

        # 创建了一张图片
        self.assertEqual(len(image_model.all()), old_count+1)

        # 关联Imageid, 等于最后一张图片的id
        item = imgitem_model.get(id)
        self.assertEqual(item.Imageid, image_model.all()[-1].id)

        # 验证getImageId和getImageUrl
        self.assertEqual(item.Imageid, imgitem_model.getImageId(id))
        self.assertEqual(item.image.url, imgitem_model.getImageUrl(id))

        # 转换为png格式
        image_path = sh.urlToPath(item.image.url)
        self.assertTrue(image_path.endswith('/%d.png' % (item.Imageid)))
        self.assertEqual(imghdr.what(None, open(image_path).read()), 'png')

        # 压缩为50x50. 因为会保持原有比例，所以压缩后高度依然是50, 不是60
        self.assertEqual(Image.open(image_path).size, (50, 50))

    # 测试update会新建一个Image并关联，删除原Image数据，但不删除原Image文件
    def test_update(self):
        imgitem_model.use_convert = True
        imgitem_model.convert_type = 'png'
        imgitem_model.max_width = 50
        imgitem_model.max_height = 60

        # 插入ImgItem数据
        data = sh.copy(test_data)
        data[image_model.image_key] = test_image_data
        id = imgitem_model.insert(data)

        item = imgitem_model.get(id)
        old_image_id = item.Imageid
        old_image_path = image_model.getFilePath(old_image_id)
        old_image_value = open(old_image_path).read()

        # 更新图片数据
        imgitem_model.convert_type = 'jpg' # update时改为jpg
        imgitem_model.update(id, data)
        item2 = imgitem_model.get(id)
        new_image_id = item2.Imageid
        new_image_path = image_model.getFilePath(new_image_id)

        # update时新建了Image
        self.assertEqual(old_image_id + 1, new_image_id)
        # 删除原Image数据
        self.assertIsNone(image_model.get(old_image_id))
        # 保留原图片文件
        self.assertTrue(os.path.exists(old_image_path))
        self.assertEqual(open(old_image_path).read(), old_image_value)
        # 新图片为jpg格式
        self.assertTrue(new_image_path.endswith('/%d.jpg' % (new_image_id)))
        self.assertEqual(imghdr.what(None, open(new_image_path).read()), 'jpeg')
        
    # 可以通过__ignore_convert_image显示声明不转换图片
    def test_ignore_convert_image(self):
        imgitem_model.use_convert = True
        imgitem_model.convert_type = 'png'
        imgitem_model.max_width  = 50
        imgitem_model.max_height = 60
        data = sh.copy(test_data)
        data[image_model.image_key] = test_image_data
        data['__ignore_convert_image'] = True
        id = imgitem_model.insert(data)
        item = imgitem_model.get(id)
        image_path = sh.urlToPath(item.image.url)
        # 保存的文件数据与测试数据一致, 文件没有被convert
        self.assertEqual(open(image_path).read(), test_image_data.value)
