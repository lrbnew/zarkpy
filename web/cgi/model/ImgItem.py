#!/usr/bin/env python
#coding=utf-8
import sys, os
if __name__=='__main__':
    father_dir = os.path.split(os.path.realpath(__file__))[0].rpartition('/')[0]
    if father_dir not in sys.path:
        sys.path.insert(0, father_dir)

from Model import Model
import site_helper as sh

# 带有一张图片的model
# table_name和item_id与Image表的data_name和data_id关联

class ImgItem(Model):
    table_name      = ''
    column_names    = ['Imageid', ]
    use_convert     = False # 是否压缩以及修改图片
    max_width       = None  # 压缩后最大宽度
    max_height      = None  # 压缩后最大高度 (宽和高都不为None时才压缩图片)
    convert_type    = 'jpg' # 保存的目标格式,为None则保持原格式
    convert_gif     = False # 是否转换gif图片，如果是，则仅取第一帧
    convert_quality = None  # 保存的目标质量,小于100时压缩,1表示最差
    remove_info     = False # 是否删除附加信息,能减小文件大小,但可能影响图片质量

    def insert(self, data):
        assert(self.table_name != '')
        data = sh.copy(data)
        img_model = sh.model('Image')

        new_id = Model.insert(self, data)

        if data.has_key(img_model.image_key):
            img_id = img_model.insert(data)
            Model.update(self, new_id, {'Imageid': img_id})
            img_model.update(img_id, {'data_id': new_id, 'data_name': self.table_name})
            # convert image
            ignore_covert = data.get('__ignore_convert_image', False)
            if self.use_convert and not ignore_covert:
                self.convertImage(data, img_id)

        return new_id

    def convertImage(self, data, img_id):
        img_model = sh.model('Image')
        file_path = img_model.getFilePath(img_id)
        convert_path = img_model.convertImage(file_path, self.convert_type, max_width=self.max_width, max_height=self.max_height, convert_quality=self.convert_quality, remove_info=self.remove_info, convert_gif=self.convert_gif)
        if file_path != convert_path:
            os.system('rm "%s"' % file_path)
            img_model._updateUrl(data, img_id, convert_path.rpartition('.')[2])
        return convert_path

    def update(self, item_id, data):
        img_model = sh.model('Image')
        if data.has_key(img_model.image_key):
            if self.getImageId(item_id):
                img_model.delete(self.getImageId(item_id))
            img_id = img_model.insert(data)
            data['Imageid'] = img_id
            img_model.update(img_id, {'data_id': item_id, 'data_name': self.table_name})
            # convert image
            ignore_covert = data.get('__ignore_convert_image', False)
            if self.use_convert and not ignore_covert:
                self.convertImage(data, img_id)
        return Model.update(self, item_id, data)

    def getImageUrl(self, item_id):
        exists = self.get(item_id)
        return exists.image.url if exists and exists.image else ''

    def getImageId(self, item_id):
        exists = self.get(item_id)
        return exists.Imageid if exists else None

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Imageid         int unsigned not null default 0,
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''

if __name__=='__main__':
    usage = 'Usage: python model/ImgItem.py insert model_name img_file'
    argv = [a for a in sys.argv if not a.startswith('-')]

    if len(argv) != 4 or argv[1] != 'insert':
        print usage
        exit(1)
    file_path = argv[3]
    if not os.path.exists(file_path):
        print 'ERROR: image file is not exists'
        exit(1)
    try:
        model = sh.model(argv[2])
    except:
        print 'ERROR: model is not exists?'
        exit(1)

    import imghdr
    image_content = value=open(file_path).read()
    image_type = imghdr.what(None, image_content)
    image_file = dict(filename=file_path, value=image_content, imagetype=image_type)
    data = {sh.model('Image').image_key: sh.storage(image_file)}
    data.update(dict([a[2:].split('=') for a in sys.argv if a.startswith('--') and '=' in a]))
    model.insert(data)
