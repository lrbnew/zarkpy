#!/usr/bin/env python
#coding=utf-8
import sys, os
# 导入cgi目录
if __name__=='__main__':
    father_dir = os.path.split(os.path.realpath(__file__))[0].rpartition('/')[0]
    if father_dir not in sys.path:
        sys.path.insert(0, father_dir)

from Model import Model
import site_helper as sh
# 保存用户的设置，比如/my/stat页面用于设置统计代码，则type就等于stat

class Setting(Model):
    table_name = 'Setting'
    column_names = ['Userid', 'type', 'value', ]
    decorator = [
        ('NotEmpty', dict(not_empty_attrs=['Userid', 'type',]) ),
    ]

    def setValue(self, Userid, type, value):
        exists = self.getOneByWhere('Userid=%s and type=%s', Userid, type)
        if exists:
            return self.update(exists.id, {'value': value})
        else:
            return self.insert(dict(Userid=Userid, type=type, value=value))

    table_template = \
        '''CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            Userid          int unsigned not null,
            type            varchar(30)  not null,
            value           text charset utf8 not null,
            primary key     ({$table_name}id),
            unique key      (Userid, type)
        )ENGINE=InnoDB; '''

def _operateSetting(argv, usage, actions):
    try:
        assert len(argv) == 4 or len(argv) == 5
        assert argv[1] in actions
        if len(argv) == 4:
            argv.append('')
        action, email, key, value = argv[1:]
        user_model = sh.model('User')
        setting_model = sh.model('Setting')

        user = user_model.getByEmail(email)
        if not user:
            print 'ERROR: user %s is not exists' % email
            exit(0)

        exists = setting_model.getOneByWhere('Userid=%s and type=%s', user.id, key)

        if action == 'get':
            if exists:
                print exists.value

        elif action == 'set':
            if exists:
                setting_model.update(exists.id, {'value': value})
            else:
                setting_model.insert({'Userid': user.id, 'type': key, 'value': value})
        
        elif action == 'delete':
            if exists:
                setting_model.delete(exists.id)

    except Exception:
        print usage

if __name__=='__main__':
    usage = 'Usage: python model/Setting.py {set|get|delete}'
    usage += '\n   set email key value'
    usage += '\n   get email key'
    usage += '\n   delete email key'
    _operateSetting(sys.argv, usage, ['set', 'get', 'delete'])
