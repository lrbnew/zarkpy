#coding=utf-8
import os
import site_helper as sh
from Model import ModelData
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

'''
如何在model中包含子文件夹?
比如你想把部分model文件放到model/sub中去，那么可以按照以下步骤做:
1 新建model/sub文件夹，并把以上代码复制到model/sub/__init__.py文件中
2 然后在下面添加一句: import sub
3 把model/sub/__init__.py中的 from Model import ModelData这句话改为: from .. import ModelData
4 给tool/init_database.py文件中的INIT_DIR添加'model/sub'值
'''
