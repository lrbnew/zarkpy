#!/usr/bin/env python
#coding=utf-8
# 项目重命名，如果你在项目中的某个文件中包含了项目名称，那么应该把那个文件加入RENAME_FILES
# 你应该遵循先rename，后生成git仓库，再共享和发布
import os
import sys

RENAME_FILES = ['conf/nginx/exp', 'conf/nginx/master', 'doc/sql/init_database.sql', 'tool/auto_restart.py', 'tool/export.sh', 'tool/export_first.sh', 'tool/install.sh', 'tool/launch-exp.sh', 'tool/launch.sh', 'tool/set_git_to_share.sh', 'web/cgi/site_helper.py', 'tool/reset_port.py',]

if __name__=='__main__':
    if len(sys.argv) == 3:
        old_name = sys.argv[1]
        new_name = sys.argv[2]
        this_file_path = os.path.split(os.path.realpath(__file__))[0]
        if new_name in this_file_path.split('/'): 
            project_root = this_file_path.partition(new_name)[0] + new_name + '/'
            print '把以下文件中的"%s"字符串替换为"%s"' % (old_name, new_name)
            for file_name in RENAME_FILES:
                file_path = project_root + file_name
                print file_path
                os.system('''sed -i "" -e "s/%s/%s/g" "%s"''' % (old_name, new_name, file_path))
            also_count = os.popen('grep "%s" -rl "%s" | wc -l' % (old_name, project_root)).read().strip()
            print '\n替换后在%s中找到包含"%s"字符串的文件: %s 个' % (project_root, old_name, also_count)
            if also_count != '0':
                print '请使用下面的命令搜索依然包含"%s"字符串的文件，确保改名完整' % old_name
                print 'grep "%s" -rl "%s"' % (old_name, project_root)
        else:
            print '请先: mv /opt/old_name /opt/new_name'
            print '然后: python /opt/new_name/tool/rename.py old_name new_name'
    else:
        print 'Usage: python /opt/your_project/tool/rename.py old_name new_name'
        print 'rename之前,建议先备份原代码'
