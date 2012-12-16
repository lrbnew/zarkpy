#coding=utf-8
import sys, os
if __name__=='__main__':
    sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0].rpartition('/')[0])

from User import User
import site_helper as sh

class AdminUser(User):
    table_name = 'AdminUser'
    column_names = ['email','name','password']

    decorator = [
        ('NotEmpty', dict(not_empty_attrs=['email', 'name', 'password']) ),
        ('StringProcess', dict(lower=['email'], strip=['email']) )
    ]

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            email           varchar(100) not null,
            name            varchar(32)  charset utf8 not null,
            password        varchar(32)  not null,
            primary key ({$table_name}id),
            unique key (email),
            key (name)
        )ENGINE=InnoDB;'''


if __name__=='__main__':
    usage = 'Usage: python model/AdminUser.py {add|delete|resetpassword|name|show}'
    usage += '\n   add email name password'
    usage += '\n   delete email'
    usage += '\n   resetpassword email new_password'
    usage += '\n   name email new_name'
    usage += '\n   show email'
    import User as UserModule
    UserModule._operateUser(sh.model('AdminUser'), sys.argv, usage, 
        ['add', 'delete', 'resetpassword', 'name', 'show',])
