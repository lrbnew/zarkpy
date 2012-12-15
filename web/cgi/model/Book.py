#coding=utf-8
from ImgText import ImgText

class Book(ImgText):
    table_name      = 'Book'
    column_names    = ['Imageid', 'title', ]
    max_width       = 500  # 压缩后最大宽度
    max_height      = 500  # 压缩后最大高度 (宽和高都不为None时才压缩图片)
    convert_type    = 'jpg' # 保存的目标格式,为None则不转换
    convert_gif     = False # 是否转换gif图片，如果是，则仅取第一帧
    convert_quality = 20  # 保存的目标质量,小于100时压缩,1表示最差
    remove_info     = True  # 是否删除附加信息,能减小文件大小,但不影响图片质量

    decorator = [
        ('Orderby',   dict(orderby='{$primary_key} desc') ),
        ('Pagination',dict(paging_key='page_num', paging_volume=3, paging=True) ),
        ('EmptyModel', dict() ),
        ('StringProcess', dict(strip=['title'], lower=['title']) )
    ]

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Imageid         int unsigned not null default 0,
            title           varchar(100) charset utf8 not null default '',
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''
