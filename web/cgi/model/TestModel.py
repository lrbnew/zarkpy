#coding=utf-8
from Model import Model

class TestModel(Model):
    table_name = 'TestModel' 
    column_names = ['title']
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            title varchar(100) not null default '',
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''
