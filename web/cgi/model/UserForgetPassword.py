#coding=utf-8
# 重置用户密码的验证码
from Model import Model

class UserForgetPassword(Model):
    table_name = 'UserForgetPassword'
    column_names = ['Userid', 'code', ]
    expires = 3600 * 24 # 验证码过期时间

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Userid          int unsigned not null,
            code            varchar(32)  not null,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            unique key (Userid)
        )ENGINE=InnoDB;
        '''
