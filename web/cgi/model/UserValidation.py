#coding=utf-8
import time
from Model import Model
import site_helper as sh

# 验证用户邮箱的验证码

class UserValidation(Model):  
    table_name = 'UserValidation'
    column_names = ['Userid', 'code', ]

    table_template = '''
        CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Userid          int unsigned not null,
            code            varchar(32)  not null,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            unique key (Userid)
        )ENGINE=InnoDB;
        '''
