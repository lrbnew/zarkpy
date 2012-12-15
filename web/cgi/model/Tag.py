#coding=utf-8
from Model import Model

class Tag(Model):
    table_name = 'Tag'
    column_names = ['data_name', 'data_id', 'name', ]

    table_template = \
        '''CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            data_name       varchar(30)  not null,
            data_id         int unsigned not null,
            name            varchar(100) charset utf8 not null,
            primary key     ({$table_name}id),
            unique key      (data_name, data_id, name),
            key             (data_name, name)
        )ENGINE=InnoDB; '''
