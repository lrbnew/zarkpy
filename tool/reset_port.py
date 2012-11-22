#!/usr/bin/env python
#coding=utf-8
# 修改项目端口号，每次修改一个端口
import os
import sys

REPORT_FILES = ['conf/nginx/master', 'conf/nginx/exp', 'tool/export.sh', 'tool/launch.sh', 'tool/launch-exp.sh', 'web/cgi/site_helper.py',]

if __name__=='__main__':
    if len(sys.argv) == 3:
        old_port = sys.argv[1]
        new_port = sys.argv[2]
        this_file_path = os.path.split(os.path.realpath(__file__))[0]
        project_root = this_file_path.rstrip('/').rpartition('/')[0] + '/'
        print '把以下文件中的"%s"字符串替换为"%s"' % (old_port, new_port)
        for file_name in REPORT_FILES:
            file_path = project_root + file_name
            print file_path
            os.system('''sed -i "" -e "s/%s/%s/g" "%s"''' % (old_port, new_port, file_path))
        also_count = os.popen('grep "%s" -rl "%s" | wc -l' % (old_port, project_root)).read().strip()
        print '\n替换后在%s中找到包含"%s"字符串的文件: %s 个' % (project_root, old_port, also_count)
        if also_count != '0':
            print '请使用下面的命令搜索依然包含"%s"字符串的文件，确保修改了所有地方的端口号' % old_port
            print 'grep "%s" -rl "%s"' % (old_port, project_root)
    else:
        print 'Usage: python /opt/zarkpy/tool/reset_port.py old_port new_port'
        print 'reset port之前,建议先备份原代码'

