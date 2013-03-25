#coding=utf-8
from ImgItem import ImgItem

# 后台图片中心，包含各个页面可能用到的素材，富文本上传的图片

class EditorImage(ImgItem):
    table_name = 'EditorImage'
    column_names = ['Imageid', 'title']

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Imageid         int unsigned  not null default 0,
            title           varchar(100)  charset utf8 not null default '',
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''
