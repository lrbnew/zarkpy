#coding=utf-8
from Model import Model

# 网站的配置信息

class SiteConfig(Model):
    table_name = 'SiteConfig'
    column_names = ['name', 'value', ]

    table_template = \
        '''CREATE TABLE {$table_name} (
           {$table_name}id  int unsigned not null auto_increment,
           name             varchar(100) not null default '',
           value            text charset utf8,
           primary key      ({$table_name}id),
           unique key       (name)
        )ENGINE=InnoDB; '''
