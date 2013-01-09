#coding=utf-8
from Model import Model

# 保存用户的session
# 默认情况下session是保存在磁盘文件中的，路径在sh.config.SESSION_PATH中配置，但如果你的访问量比较大，那么可能需要把session保存在mysql数据库中，仅需把app.py中的session初始化改为如下即可:
# session_db = web.database(dbn='mysql', db=sh.config.DB_DATABASE, user=sh.config.DB_USER, pw=sh.config.DB_PASSWORD)
# sh.session = web.session.Session(app, web.session.DBStore(session_db, 'Session'), initializer=default_session)
class Session(Model):
    table_name = '' # 默认不使用
    #table_name = 'Session' 使用数据库保存session
    column_names = ['session_id', 'atime', 'data']
    table_template = \
        ''' CREATE TABLE {$table_name} (
            session_id char(128) not null,
            atime timestamp not null default current_timestamp,
            data text,
            unique key (session_id)
        )ENGINE=InnoDB; '''
