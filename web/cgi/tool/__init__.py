import os
import site_helper as sh

EXCEPT_FILES = ['__init__']
for module_name, module in sh.getDirModules(os.path.split(os.path.realpath(__file__))[0], __name__, except_files=EXCEPT_FILES):
    exec('%s = module' % module_name)
