#coding=utf-8
import site_helper, os

# 自动导入model文件夹中的所有class
# 作用相当于 "from User import User" + "from Model import Model" + ....
EXCEPT_FILES = ['__init__', ]
for module_name, module in site_helper.getDirModules(os.path.split(os.path.realpath(__file__))[0], __name__, except_files=EXCEPT_FILES):
    exec('%s = module' % module_name)
