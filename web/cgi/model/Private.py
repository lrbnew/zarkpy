#coding=utf-8
from Model import Model

# 提供给modeldecorator/Private.py使用，记录每个用户在每种数据中的当前private_id

class Private(Model):
    table_name = 'Private'
    column_names = ['data_name', 'user_id', 'private_id', ]

    def getNextPrivateid(self, data_name, user_id):
        exists = self.getOneByWhere('data_name=%s and user_id=%s', [data_name, user_id])
        return exists.private_id + 1 if exists else 1

    def incPrivateid(self, data_name, user_id):
        exists = self.getOneByWhere('data_name=%s and user_id=%s', [data_name, user_id])
        if not exists:
            self.insert(dict(data_name=data_name, user_id=user_id, private_id=1))
            return 1
        else:
            self.update(exists.id, dict(private_id = exists.private_id+1))
            return exists.private_id + 1

    def resetPrivateid(self, data_name, user_id):
        exists = self.getOneByWhere('data_name=%s and user_id=%s', [data_name, user_id])
        return self.delete(exists.id) > 0 if exists else False

    table_template = \
        '''CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            data_name       varchar(30)  not null,
            user_id         int unsigned not null,
            private_id      int unsigned not null,
            primary key     ({$table_name}id),
            unique key      (user_id, data_name)
        )ENGINE=InnoDB; '''
