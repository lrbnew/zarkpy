#coding=utf-8
import web
import copy
import re
import site_helper as sh
from DBHelper import DBHelper

class Model: # 子类的calss名称必须与文件名一致,包括大小写
    # 数据表名,应该与class名称和文件名一致,否则需同时修改primary_key
    # 为空则不自动创建表
    table_name = '' 
    column_names = []  # 需要自动insert或update的字段列表,子类不能为空
    primary_key = None # 表的主键名，不推荐修改
    decorator = []     # 此model使用的装饰器，详见modeldecorator模块

    def __init__(self):
        if self.primary_key == None:
            self.primary_key = self.table_name+'id'
        try:
            assert(type(self.table_name) is str)
            assert(len (self.table_name) > 0)
            assert(' ' not in self.table_name )
        except:
            print 'the table_name is:', self.table_name
            print 'and the class is:', self.__class__
            raise
        assert(type(self.primary_key) is str)
        assert(len(self.primary_key) > 0)
        assert(type(self.column_names) is list)
        assert(len(self.column_names) > 0) # column_names不能为空
        self.db = DBHelper()

    # 插入一个数据，type(data)为dict或web.Storage
    # 返回新数据的主键值(primary key)
    def insert(self, data):
        data = self._formatInsertData(data)
        data = self._removeNone(data)
        assert(data is not None)
        self._insertValidate(data)
        insert_cols =   [c       for c in self.column_names if c in data.keys()]
        insert_values = [data[c] for c in self.column_names if c in data.keys()]
        query = 'insert into %s (%s) values (%s)' % (self.table_name, ','.join(insert_cols), ','.join(len(insert_cols)*['%s']))
        return self.db.insert(query, tuple(insert_values))

    # 替换插入，当primary key或者某个unique key冲突时，即替换原有数据
    # 注意替换后primary key会被更新, 并返回此值
    def replaceInsert(self, data):
        data = self._formatInsertData(data)
        data = self._removeNone(data)
        assert(data is not None)
        self._insertValidate(data)
        insert_cols =   [c       for c in self.column_names if c in data.keys()]
        insert_values = [data[c] for c in self.column_names if c in data.keys()]
        query = 'replace into %s (%s) values (%s)' % (self.table_name, ','.join(insert_cols), ','.join(len(insert_cols)*['%s']))
        return self.db.insert(query, tuple(insert_values))

    def update(self, item_id, data):
        try:
            data = self._formatUpdateData(data)
            data = self._removeNone(data)
            assert(data is not None)
            self._updateValidate(data)
            update_cols =   [c       for c in self.column_names if c in data.keys()]
            update_values = [data[c] for c in self.column_names if c in data.keys()]
            assert(len(update_cols) == len(update_values) > 0 )
            query = 'update '+self.table_name \
                    + ' set ' + ','.join([c+'=%s' for c in update_cols]) \
                    + ' where '+ self.table_name + 'id=%s'
            affected = self.db.update(query, update_values + [item_id])
        except:
            print 'ERROR INFO:'
            print 'data is :', data
            raise
        return affected

    def delete(self, item_id):
        return self.db.delete('delete from ' + self.table_name + ' where ' + self.table_name + 'id=%s', item_id)

    def get(self, item_id):
        return self.db.fetchOne('select * from ' + self.table_name + ' where ' + self.table_name + 'id=%s limit 1', item_id)

    def gets(self, item_ids):
        assert(type(item_ids) is list)
        if len(item_ids) > 0:
            where = ' or '.join([self.table_name+'id=%s'] * len(item_ids))
            return self.db.fetchSome('select * from ' + self.table_name + ' where ' + where, item_ids)
        else:
            return []

    # 根据env dict返回多个数据的list
    # env的可选参数以及样例分别有:
    # select: username, email
    # from: User
    # join 
    # where: ('age>%s', (18,))
    # orderby: 'Userid desc'
    # limit: (0, 10)
    # distinct: True
    def all(self, env=None):
        query_string, argv = self._spliceQuery(env)
        return self.db.fetchSome(query_string, argv)

    def getOneByWhere(self, where, argv=[]):
        assert(type(argv) in [list,tuple])
        return self.db.fetchOne('select * from ' + self.table_name + ' where ' + where + ' limit 1', argv)

    # 根据env获得数据量
    def getCount(self, env={}):
        new_env = self._copyData(env) # 不改变原env
        new_env['select'] = 'count(*)' 
        if new_env.has_key('limit'):
            del new_env['limit'] # mysql语法中, count(*)和limit不能一起用
        query_string, argv = self._spliceQuery(new_env)
        return self.db.fetchFirst(query_string, argv)

    # 获得model的装饰器的属性
    def getDecoratorAttr(self, attr):
        if hasattr(self, '_decorator_model'):
            assert(self._decorator_model is not None)
            return getattr(self._decorator_model, attr)
        else:
            return getattr(self, attr)

    # 使用table_template字段创建数据表
    def createTable(self):
        assert(len(self.table_name)>0)
        assert(len(self.table_template)>0)
        assert(not DBHelper().isTableExists(self.table_name))
        try:
            formated_creat_query = self._getCreateTableQuery()
            self.db.executeQuery(formated_creat_query)
        except:
            print formated_creat_query
            raise

    # 根据table_template在原有表上添加新字段, 但不添加新的索引(为了保证线上数据稳定)
    def increaseCreateTable(self):
        assert(len(self.table_name)>0)
        assert(len(self.table_template)>0)
        assert(DBHelper().isTableExists(self.table_name))
        def getColumnsFromSQL(sql):
            sql = sql.partition('(')[2].rpartition(')')[0].replace('\n', ' ').replace('\r', ' ')
            columns = []
            column = []
            bracket_count = 0
            for c in sql+',':
                if c == '(':
                    bracket_count += 1
                    column.append(c)
                elif c == ')':
                    bracket_count -= 1
                    column.append(c)
                elif bracket_count == 0 and c==',':
                    column = ''.join(column)
                    if column.strip().split()[0].lower() not in ['key', 'primary', 'unique'] and column.strip().split('(')[0].lower() not in ['key', 'primary', 'unique']:
                        columns.append((column.strip().split()[0], column))
                    column = []
                else:
                    column.append(c)
                if bracket_count < 0:
                    raise Exception('table template is invalid. model name is: ' + self.table_name)
            return columns
        try:
            exists_columns = sh.getDBHelper().getTableColumns(self.table_name)
            formated_creat_query = self._getCreateTableQuery()
            columns = getColumnsFromSQL(formated_creat_query)
            for column_name, query  in columns:
                if column_name.lower() not in map(str.lower, exists_columns):
                    try:
                        self.db.executeQuery('alter table %s add %s' % (self.table_name, query))
                    except:
                        print 'alter query is:'
                        print 'alter table %s add %s' % (self.table_name, query)
                        raise
        except:
            print 'formated creat query is:'
            print formated_creat_query
            raise

    # 对insert的数据进行预处理
    def _formatInsertData(self, data):
        return data

    # 对update的数据进行预处理
    def _formatUpdateData(self, data):
        return data

    # 对insert的数据进行断言
    def _insertValidate(self, data):
        pass

    # 对update的数据进行断言
    def _updateValidate(self, data):
        pass

    def _removeNone(self, data):
        ret_data = self._copyData(data)
        for k,v in data.items():
            if v is None:
                del ret_data[k]
        return ret_data

    def _copyData(self, data):
        ret_data = web.Storage({})
        for k in data.keys():
            ret_data[k] = copy.copy(data[k])
        return ret_data

    def _getCreateTableQuery(self):
        ret_query = self.table_template
        for variable in re.compile('{\$\w+}').findall(self.table_template):
            ret_query = ret_query.replace(variable, getattr(self, variable[2:-1]))
        return ret_query

    def replaceAttr(self, query):
        pass

    # 使用env生成query_string和argv
    # 注意，不能把env的默认值改为{}, 否则env将成为_spliceQuery函数的一个全局属性
    def _spliceQuery(self, env=None):
        if env is None: env = {}
        query_string = 'select '
        argv = []
        assert(type(env) in [dict, web.Storage])

        if env.get('select', None):
            query_string += env['select'] + ' '
        else:
            if env.get('distinct', None):
                query_string += 'distinct '
            query_string += '* '

        if env.get('from', None):
            query_string += 'from '+ env['from'] + ' '
        else:
            query_string += 'from '+ self.table_name + ' '

        if env.get('where', None) != None: # { 'where': ('title=%s',['test']) }
            assert( type(env['where']) in (tuple, list) and  len(env['where']) == 2 )
            assert( type(env['where'][0]) is str )
            assert( type(env['where'][1]) in (tuple, list) )
            query_string += ' where ' + env['where'][0] + ' '
            argv.extend(env['where'][1])

        if env.get('orderby', None):
            query_string += ' order by '+env.get('orderby')

        if env.get('limit', None):
            assert( type(env['limit']) in (tuple, list) and  len(env['limit']) == 2 )
            #assert( (type(env['limit'][0]) and type(env['limit'][1])) in [int,long] )
            query_string += ' limit %s, %s'
            argv.append(env['limit'][0])
            argv.append(env['limit'][1])

        return query_string, argv

    # table_template变量名不能以下划线"_"开头，因为_开头的“类静态”数据将不会被子类overwrite
    # 而Model要求每个子类会调用自己的table_template变量，而不使用父类的
    table_template = \
        ''' CREATE TABLE {$table_name} (
            {$table_name}id int unsigned not null auto_increment,
            primary key ({$table_name}id)
        )ENGINE=InnoDB; '''
