#coding=utf-8
from Model import Model

# 提供给modeldecorator/Private.py使用，记录每个用户在每种数据中的当前private_id

class Private(Model):
    table_name = 'Private'
    column_names = ['data_name', 'user_id', 'private_id', ]

    def getPrivateid(self, data_name, user_id):
        exists = self.getOneByWhere('data_name=%s and user_id=%s', [data_name, user_id])
        if not exists:
            id = self.insert(dict(data_name=data_name, user_id=user_id, private_id=0))
            p_id = 1
        else:
            id = exists.id
            p_id = exists.private_id + 1
        self.update(id, dict(private_id = p_id))
        return p_id

    table_template = \
        '''CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            data_name       varchar(30)  not null,
            user_id         int unsigned not null,
            private_id      int unsigned not null,
            primary key     ({$table_name}id),
            unique key      (user_id, data_name)
        )ENGINE=InnoDB; '''
