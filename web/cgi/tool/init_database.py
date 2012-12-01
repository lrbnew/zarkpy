#coding=utf8
import site_helper, sys, glob, re

INIT_DIR = ['model',] # 需要自动创建表的文件夹, 不会递归处理，需要手动添加子文件夹
PRIORITY = [] # 优先创建表的model列表，用于_sort函数

# 把file_paths中的preference_list值排到前面来,应对自动创建数据库表时的外键依赖
def _sort(file_paths, preference_list):
    ret_pre_paths = []
    ret_other_paths = []
    for file_path in file_paths:
        model_name = file_path.rpartition('/')[2].rpartition('.')[0]
        if model_name in preference_list:
            ret_pre_paths.append(file_path)
        else:
            ret_other_paths.append(file_path)
    return ret_pre_paths + ret_other_paths

# 用model中class的table_template变量新建表
def initTables():
    exists_tables = _getExistsTables()

    for dir_name in INIT_DIR:
        file_paths = glob.glob(site_helper.config.APP_ROOT_PATH+('web/cgi/%s/*.py' % dir_name))
        file_paths = _sort(file_paths, PRIORITY)
        for file_path in file_paths:
            model_name = file_path.rpartition('/')[2].rpartition('.')[0]
            # 去掉_开头的文件, 任何hasattr(module,'__init__')都等于True
            if model_name[0] != '_':
                try:
                    __import__(dir_name.replace('/', '.').strip('.')+'.'+model_name)
                except:
                    print 'try to import %s' % (dir_name.replace('/', '.').strip('.')+'.'+model_name)
                    raise
                if hasattr(sys.modules[dir_name.replace('/', '.').strip('.')], model_name):
                    model_class = getattr(sys.modules[dir_name.replace('/', '.').strip('.')],model_name)
                    if hasattr(model_class, 'table_template') and len(model_class.table_name) > 0:
                        try:
                            model_instance = model_class()
                            if model_class.table_name:
                                if model_class.table_name not in exists_tables:
                                    model_instance.createTable()
                                else:
                                    model_instance.increaseCreateTable()
                        except:
                            print 'model_class is:', model_class
                            print 'table_name is:', model_class.table_name
                            raise

def _getExistsTables():
    return site_helper.getDBHelper().fetchSomeFirst('show tables', ignore_assert=True)

def initDatas():
    query = open(site_helper.config.APP_ROOT_PATH + 'web/cgi/tool/init_datas.sql').read().strip()
    site_helper.getDBHelper().executeQuery(query)
