#coding=utf-8
from ImgItem import ImgItem

# 图文数据类，常用于各种带有一张图片的类的基类

class ImgText(ImgItem):
    table_name = ''
    column_names = ['Imageid', 'title', 'content']

    decorator = [
        ('Orderby',{'orderby':'{$primary_key} desc'}),
    ]

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Imageid         int unsigned  not null default 0,
            title           varchar(100)  charset utf8 not null default '',
            content         varchar(1000) charset utf8 not null default '',
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            key (title)
        )ENGINE=InnoDB; '''
