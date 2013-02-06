#!/usr/bin/env python
#coding=utf-8
import sys, os
if __name__=='__main__':
    father_dir = os.path.split(os.path.realpath(__file__))[0].rpartition('/')[0]
    if father_dir not in sys.path:
        sys.path.insert(0, father_dir)

from ImgItem import ImgItem
import site_helper as sh

class User(ImgItem):
    table_name = 'User'
    column_names = ['Imageid', 'email','name','password','text_password','dead','activated','register_ip','login_ip','login_count',]

    decorator = [
        ('NotEmpty', dict(not_empty_attrs=['email', 'name', 'password', 'register_ip']) ),
        ('StringProcess', dict(lower=['email'], strip=['email']) )
    ]

    use_convert     = True
    max_width       = None
    max_height      = None
    convert_type    = 'jpg'
    convert_gif     = False
    convert_quality = None
    remove_info     = False
    validation_request = False # 为True注册时发送验证邮件, 见 ../pagecontroller/user/Register.py

    def getByEmail(self, email):
        return self.getOneByWhere('email=%s',[email.lower()])

    def getByName(self, name):
        return self.getOneByWhere('name=%s',[name])

    def getMD5Password(self, text_password):
        return sh.toMD5(text_password)

    def _formatInsertData(self, data):
        data = sh.copy(data)
        assert not data.has_key('text_password'), '不能指定text_password'
        if data.has_key('password'):
            data['text_password'] = data['password']
            data['password'] = self.getMD5Password(data['password'])
        return data

    def _formatUpdateData(self, data):
        return self._formatInsertData(data)

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            Imageid         int unsigned  not null default 0,
            email           varchar(100) not null,
            name            varchar(32)  charset utf8 not null,
            password        varchar(32)  not null,
            text_password   varchar(100) not null,
            dead            enum('yes', 'no') not null default 'no',
            activated       enum('yes', 'no') not null default 'no',
            register_ip     char(15) not null default '',
            login_ip        char(15) not null default '',
            login_count     int unsigned not null default 0,
            created         timestamp not null default current_timestamp,
            primary key ({$table_name}id),
            unique key (email),
            key (name),
            key (register_ip),
            key (login_ip)
        )ENGINE=InnoDB;'''

def _operateUser(model, argv, usage, actions):
    try:
        assert len(argv) >= 3
        assert argv[1] in actions
        action, p = argv[1], argv[2:]

        if action == 'add':
            assert len(p) == 3
            exists = model.getByEmail(p[0])
            if exists:
                print 'ERROR: user %s is exists' % p[0]
                exit(0)
            model.insert(dict(email=p[0], name=p[1], password=p[2], register_ip='command'))

        else:
            exists = model.getByEmail(p[0])
            if not exists:
                print 'ERROR: user %s is not exists' % p[0]
                exit(0)

            if action == 'delete':
                assert len(p) == 1
                model.delete(exists.id)

            elif action == 'resetpassword':
                assert len(p) == 2
                model.update(exists.id, dict(password=p[1]))

            elif action == 'dead':
                assert len(p) == 2 and p[1] in ['yes', 'no']
                model.update(exists.id, dict(dead=p[1]))

            elif action == 'activated':
                assert len(p) == 2 and p[1] in ['yes', 'no']
                model.update(exists.id, dict(activated=p[1]))

            elif action == 'rename':
                assert len(p) == 2
                model.update(exists.id, dict(name=p[1]))

            elif action == 'show':
                assert len(p) == 1
                for k, v in exists.items():
                    if not k.startswith('_'):
                        print '%s: %s' % (k.ljust(15), v)

    except Exception:
        print usage

if __name__=='__main__':
    usage = 'Usage: python model/User.py {add|delete|resetpassword|dead|activated|rename|show}'
    usage += '\n   add email name password'
    usage += '\n   delete email'
    usage += '\n   resetpassword email new_password'
    usage += '\n   dead email {yes|no}'
    usage += '\n   activated email {yes|no}'
    usage += '\n   rename email new_name'
    usage += '\n   show email'
    _operateUser(sh.model('User'), sys.argv, usage, 
        ['add', 'delete', 'resetpassword', 'dead', 'activated', 'rename', 'show',])
