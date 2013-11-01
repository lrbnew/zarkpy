#!/usr/bin/env python
#coding=utf-8
# crontab config: * * * * * root python /opt/homework/tool/auto_restart.py 4
import os
import sys
import traceback
from datetime import datetime
ERROR_LOG = '/opt/homework/log/auto_restart'
PID_FILE  = '/var/run/homework-master-spawn-fcgi.pid'

def recodeRestart(f, count):
    f.write('restarted at %s, only %d processes alive \n'
            % (str(datetime.now()).rpartition('.')[0], count) )

if __name__=='__main__':
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
        min_num = int(sys.argv[1].strip())
        count = 0
        try:
            if os.path.exists(PID_FILE):
                for pid in open(PID_FILE).readlines():
                    pid = int(pid.strip())
                    if os.path.exists('/proc/%d' % pid):
                        count += 1
            if count < min_num:
                os.system('/opt/homework/tool/launch.sh restart')
                recodeRestart(open(ERROR_LOG, 'a'), count)
        except:
            # recode exception's info to error log
            traceback.print_exc(file=open(ERROR_LOG, 'a'))
    else:
        print 'Usage: python /opt/homework/tool/auto_restart.py min_num'
        print 'min_num: 允许的最少进程数，低于此数则重启主程序'
