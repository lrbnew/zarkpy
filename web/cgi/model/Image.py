#coding=utf-8
import os
from Model import Model
import site_helper as sh

# Image用于保存图片数据以及插入图片文件,如果需要一个带有图片功能的model,可以让你的model把图片相关的操作委托给Image.py，而不是继承Image。比如ImgItem类
# 如果你需要另一张表来存放图片数据，那么可以考虑继承Image.py，并重写_getSaveDir和_getUrlBase函数，以提供另一个文件夹存放图片文件
# 图片文件是不能修改和删除的,因此请勿在重写update函数时修改图片文件

class Image(Model):
    table_name      = 'Image'
    column_names    = ['data_name', 'data_id', 'url', ]
    image_key       = 'image_file' # data中图片数据的属性名称
    use_convert     = True  # 是否压缩以及修改图片
    max_width       = None  # 压缩后最大宽度
    max_height      = None  # 压缩后最大高度 (宽和高都不为None时才压缩图片)
    convert_type    = None  # 保存的目标格式,为None则保持原格式
    convert_gif     = False # 是否转换gif图片，如果是，则仅取第一帧
    convert_quality = None  # 保存的目标质量,小于100时压缩,1表示最差
    remove_info     = False # 是否删除附加信息,能减小文件大小,可能会降低图片质量
    known_types     = ['jpg', 'jpeg', 'png', 'gif', ]

    def insert(self, data):
        new_id = Model.insert(self, data)
        # 保存图片,并压缩尺寸,压缩质量,转格式,设置url字段值
        if data.has_key(self.image_key):
            imf = data[self.image_key]
            file_path = '%s%d.%s' % (self._getSaveDir(data), new_id, imf.imagetype)
            self._saveImage(file_path, imf.value)
            self._updateUrl(data, new_id, imf.imagetype)
            if self.use_convert and not data.get('__ignore_convert_image', False):
                convert_path = self.convertImage(file_path, self.convert_type, max_width=self.max_width, max_height=self.max_height, convert_quality=self.convert_quality, remove_info=self.remove_info, convert_gif=self.convert_gif)
                if file_path != convert_path:
                    os.system('rm "%s"' % file_path)
                    self._updateUrl(data, new_id, convert_path.rpartition('.')[2])
        return new_id

    def getUrl(self, item_id):
        exists = self.get(item_id)
        return exists.url if exists else ''

    def getFilePath(self, item_id):
        url = self.getUrl(item_id)
        return sh.urlToPath(url) if url else ''
            
    # 压缩图片的尺寸、质量、转换格式、删除文件附加信息
    def convertImage(self, file_path, convert_type, **convert_info):
        ci = convert_info
        if not convert_type:
            convert_type = file_path.rpartition('.')[2]
        # 如果是把gif转为非gif
        if file_path.endswith('.gif') and convert_type != 'gif':
            if ci.get('convert_gif', False):
                convert = 'convert "%s[0]" ' % file_path
                new_path = file_path.rpartition('.')[0] + '.' + convert_type
            else:
                convert = 'convert "%s" ' % file_path
                new_path = file_path
        else:
            convert = 'convert "%s" ' % file_path
            new_path = file_path.rpartition('.')[0] + '.' + convert_type

        if ci.get('convert_quality', 0):
            convert += ' -quality %d ' % ci.get('convert_quality')
        if ci.get('max_width', 0) and ci.get('max_height', 0):
            convert += ' -resize "%dx%d>" ' % (ci.get('max_width', 0), ci.get('max_height', 0))
        if ci.get('remove_info', False):
            convert += ' +profile "*" '
        convert += ' "%s" ' % new_path
        os.system(convert)
        assert os.path.exists(new_path), 'convert生成图片失败'
        return new_path

    def _saveImage(self, file_path, image_value):
        sh.autoMkdir(file_path)
        assert(not os.path.exists(file_path))
        with open(file_path, 'w') as f:
            f.write(image_value)

    def _updateUrl(self, data, item_id, file_type):
        return self.update(item_id, {'url': '%s%d.%s' % (self._getUrlBase(data), item_id, file_type)})

    def _getSaveDir(self, data=None):
        return sh.config.UPLOAD_IMAGE_PATH + self.table_name + '/'

    def _getUrlBase(self, data=None):
        return sh.config.UPLOAD_IMAGE_URL + self.table_name + '/'

    def _insertValidate(self, data):
        assert data.has_key(self.image_key), '插入的data没有%s数据' % self.image_key
        assert data.get(self.image_key).imagetype in self.known_types, '图片类型未知'
        assert data.get(self.image_key).has_key('filename')
        assert data.get(self.image_key).has_key('value')
        assert data.get(self.image_key).has_key('imagetype')

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id     int unsigned not null auto_increment,
            data_name           varchar(20)  not null default '',
            data_id             int unsigned not null default 0,
            url                 varchar(100) not null default '',
            primary key ({$table_name}id),
            key (data_name, data_id)
        )ENGINE=InnoDB; '''
