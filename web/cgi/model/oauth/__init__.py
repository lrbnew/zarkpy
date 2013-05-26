#coding=utf-8
import os
import site_helper as sh
from .. import ModelData
# 自动导入model文件夹中的所有class
# 作用相当于 "from User import User" + "from Model import Model" + ....
EXCEPT_FILES = ['__init__', ]
for module_name, module in sh.getDirModules(os.path.split(os.path.realpath(__file__))[0], __name__, except_files=EXCEPT_FILES):
    exec('%s = module' % module_name)
    assert not ModelData.model_names.has_key(module_name.lower())
    if '.' not in __name__:
        ModelData.model_names[module_name.lower()] = module_name
    else:
        ModelData.model_names[module_name.lower()] = __name__.partition('.')[2] + '.' + module_name
