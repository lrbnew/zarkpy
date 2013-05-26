#coding=utf-8
# ../../api/UserImage.py
import site_helper as sh
from .. import AppTest

db = sh.getDBHelper()
api_url = '/api/user-image'
ui_model = sh.model('UserImage')
test_image_path = '%sweb/cgi/testing/model_test/test_image.jpg' % sh.config.APP_ROOT_PATH

class TestUserImage(AppTest.AppTest):

    def appTestSetUp(self):
        db.executeQuery('delete from %s' % ui_model.table_name)

    def test_postImage(self):
        my_id = self.register()
        # 因为flash不能传webpy_session_id，所以这里自己指定Userid，这是一个安全隐患!
        data = sh.storage(dict(action = 'postImage', Userid = my_id))
        data.Filedata = open(test_image_path).read()
        data.Filename = 'good_image.jpg'
        # 返回结果分别表示: 成功、UserImageid、url、文件名
        res = self.post(api_url, data).split(';')
        self.assertEqual(res[0], 'success') # 验证插入成功
        self.assertEqual(res[3], 'good_image') # 验证图片文件名
        new_img_id = int(res[1]) # 得到UserImage的private_id
        # 验证图片url, 图片url中的id不是private_id
        UserImageid = self.proxyDo(ui_model.get, new_img_id).UserImageid
        url = '%s%d/%d.jpeg' % (sh.config.USER_IMAGE_URL, my_id, UserImageid)
        self.assertEqual(res[2], url)
        img = self.proxyDo(ui_model.get, new_img_id)
        self.assertEqual(img.url, url)

    # 测试delete realDelete recover
    def test_delete(self):
        my_id = self.register()
        # 插入图片并得到UserImageid
        data = sh.storage(dict(action = 'postImage', Userid = my_id))
        data.Filedata = open(test_image_path).read()
        data.Filename = 'good_image.jpg'
        new_img_id = int(self.post(api_url, data).split(';')[1])
        self.assertEqual(self.proxyDo(ui_model.get, new_img_id).deleted, 'no')
        # 使用delete，其实只是把deleted改为yes
        self.get(api_url, dict(action='delete', UserImageid=new_img_id))
        self.assertEqual(self.proxyDo(ui_model.get, new_img_id).deleted, 'yes')
        # 使用recover可以把deleted改为no
        self.get(api_url, dict(action='recover', UserImageid=new_img_id))
        self.assertEqual(self.proxyDo(ui_model.get, new_img_id).deleted, 'no')
        # 使用realDelete才真正删除图片
        self.get(api_url, dict(action='realDelete', UserImageid=new_img_id))
        self.assertIsNone(self.proxyDo(ui_model.get, new_img_id))

