#coding=utf-8
# API文档说明
from Model import Model

class APIDoc(Model):
    table_name = 'APIDoc'
    column_names = ['title','content','request_url','necessary','options','example','require_login']

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id  int unsigned not null auto_increment,
            title            varchar(100) charset utf8 not null default '',
            summary          varchar(300) charset utf8 not null default '',
            content          varchar(4000) charset utf8 not null default '',
            request_url      varchar(300) not null default '',
            require_login    enum('yes', 'no') not null default 'no',
            necessary        text charset utf8,
            options          text charset utf8,
            example          varchar(300) charset utf8 not null default '',
            primary key      ({$table_name}id)
        )ENGINE=InnoDB; '''
