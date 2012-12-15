#coding=utf-8
from Model import Model

class Category(Model):
    table_name = 'Category'
    column_names = ['data_name', 'name', ]

    table_template = \
        '''CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            data_name       varchar(30)  not null,
            name            varchar(100) charset utf8 not null,
            primary key     ({table_name}id),
            unique key      (data_name, name)
        )ENGINE=InnoDB; '''
