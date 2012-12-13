#coding=utf-8
import site_helper as sh
import os
from Model import ModelData

# 自动导入model文件夹中的所有class
# 作用相当于 "from User import User" + "from Model import Model" + ....
EXCEPT_FILES = ['__init__', ]
for module_name, module in sh.getDirModules(os.path.split(os.path.realpath(__file__))[0], __name__, except_files=EXCEPT_FILES):
    exec('%s = module' % module_name)
    assert(not ModelData.table_names.has_key(module_name.lower())) # 小写的表名也不能重复
    ModelData.table_names[module_name.lower()] = module_name
