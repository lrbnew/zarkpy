#coding=utf-8
# ../../page/user/Portrait.html
# 上传与裁剪头像
import os
import site_helper as sh

class Portrait:

    def GET(self):
        if not sh.session.is_login:
            return sh.redirectToLogin(sh.getEnv('REQUEST_URI'))

        user = sh.model('User').get(sh.session.id)
        return sh.page.user.Portrait(user)

    def POST(self):
        if not sh.session.is_login:
            return sh.redirectToLogin()
        user_model = sh.model('User')
        user = user_model.get(sh.session.id)

        inputs = sh.inputs()
        assert inputs.get('action', '')

        if inputs.action == 'upload':
            if inputs.get('image_file', ''):
                self.savePortrait(sh.session.id, inputs.image_file)
            return sh.redirect('/accounts/portrait')

        elif inputs.action == 'crop':

            if not user.image:
                return sh.alert('请先上传头像')

            assert int(float(inputs.get('region_width', '0'))) > 0
            assert int(float(inputs.get('region_height', '0'))) > 0
            real_width, real_height = sh.imageSize(user.image.url) # 图片的真实宽高
            crop = inputs.crop
            region_width = int(float(inputs.region_width)) # 选择区域的宽度
            region_height = int(float(inputs.region_height)) # 选择区域的高度

            start_x  = int(crop.split()[0]) # 选中的起始位置
            start_y  = int(crop.split()[1])
            region_x  = int(crop.split()[2])# 选中的宽度
            region_y = int(crop.split()[3]) # 选中的高度
            
            # convert 裁剪区域
            region = '%dx%d+%d+%d' % (region_x * real_width / region_width, 
                                    region_y * real_height / region_height,
                                    real_width * start_x / region_width, 
                                    real_height * start_y / region_height)

            path = sh.urlToPath(user.image.url)
            os.system('convert %s -crop %s %s' % (path, region, path+'.crop'))
            user_model.update(sh.session.id, {'crop': crop})

            # 删除以前裁剪图片的各种尺寸副本
            os.system('rm %s.crop_*' % path)

            return sh.redirect('/accounts')

    def savePortrait(self, Userid, image_file):
        user_model = sh.model('User')
        user = user_model.get(Userid)

        if user.image and image_file:
            path = sh.urlToPath(user.image.url)
            os.system('rm %s' % (path+'.crop'))

        user_model.update(Userid, {sh.model('Image').image_key: image_file})

        # 自动设置裁剪区域为整个图片
        user = user_model.get(Userid) # 为了重新拿到image数据
        size = sh.imageSize(user.image.url)
        user_model.update(user.id, {'crop': '0 0 %d %d' % size})
        path = sh.urlToPath(user.image.url)
        os.system('cp %s %s' % (path, path+'.crop'))

