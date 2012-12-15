#coding=utf-8
import hashlib
from ImgItem import ImgItem
import site_helper as sh

class User(ImgItem):
    table_name = 'User'
    column_names = ['email','name','password','text_password','dead','activated','register_ip','login_ip','login_count',]

    decorator = [
        ('NotEmpty', dict(not_empty_attrs=['email', 'name', 'password', 'register_ip']) ),
    ]

    max_width       = None
    max_height      = None
    convert_type    = 'jpg'
    convert_gif     = False
    convert_quality = None
    remove_info     = True

    def getByEmail(self, email):
        return self.getOneByWhere('email=%s',[email])

    def getByName(self, name):
        return self.getOneByWhere('name=%s',[name])

    def getMD5Password(self, text_password):
        m = hashlib.md5()
        m.update(sh.config.SECRET_KEY + sh.unicodeToStr(text_password))
        return m.hexdigest()

    def _insertValidate(self, data):
        assert not data.has_key('text_password'), '不能指定text_password'

    def _updateValidate(self, data):
        self._insertValidate(data)

    def _formatInsertData(self, data):
        data = sh.copy(data)
        data.text_password = data.password
        data.password = self.getMD5Password(data.password)
        return data

    def _formatUpdateData(self, data):
        return self._formatInsertData(data)

    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned  not null auto_increment,
            email           varchar(100) not null,
            name       varchar(32)  charset utf8 not null,
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
