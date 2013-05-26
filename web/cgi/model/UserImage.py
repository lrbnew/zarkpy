#coding=utf-8
from Image import Image
import site_helper as sh

class UserImage(Image):
    table_name      = 'UserImage'
    column_names    = ['Userid', 'private_id', 'data_name', 'data_id', 'url', 'file_name', 'deleted']
    image_key       = 'image_file' # data中图片数据的属性名称
    max_width       = None  # 压缩后最大宽度
    max_height      = None  # 压缩后最大高度 (宽和高都不为None时才压缩图片)
    convert_type    = None  # 保存的目标格式,为None则不转换
    convert_gif     = False # 是否转换gif图片，如果是，则仅取第一帧
    convert_quality = None  # 保存的目标质量,小于100时压缩,1表示最差
    remove_info     = False

    decorator = [
        ('Orderby', dict(orderby='{$primary_key} desc') ),
        ('Private', dict(user_id_key='Userid', primary_key='private_id', use_private=True) ),
        ('Pagination', dict(paging_key='page_num', paging_volume=100, paging=True) ),
    ]
    test_decorator = decorator

    def _getSaveDir(self, data=None):
        assert(data.get('Userid', 0))
        return sh.config.USER_IMAGE_PATH + str(data['Userid']) + '/'

    def _getUrlBase(self, data=None):
        assert(data.get('Userid', 0))
        return sh.config.USER_IMAGE_URL + str(data['Userid']) + '/'

    def getUrlByPrivate(self, user_id, private_id):
        return self.db.fetchFirst(self.replaceAttr('select url from {$table_name} where Userid=%s and private_id=%s'), [user_id, private_id])

    # deleted=yes, 表明图片被放入回收站
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id     int unsigned not null auto_increment,
            Userid              int unsigned not null,
            private_id          int unsigned not null,
            data_name           varchar(20)  not null default '',
            data_id             int unsigned not null default 0,
            url                 varchar(100) not null default '',
            file_name           varchar(100) charset utf8 not null default '',
            deleted             enum('yes', 'no') not null default 'no',
            primary key ({$table_name}id),
            key (data_name, data_id)
        )ENGINE=InnoDB; '''
