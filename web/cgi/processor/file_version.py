#!/usr/bin/env python
#coding=utf-8
import sys, os, re
if __name__=='__main__':
    father_dir = os.path.split(os.path.realpath(__file__))[0].rpartition('/')[0]
    if father_dir not in sys.path:
        sys.path.insert(0, father_dir)

import site_helper as sh

''' 使用正则表达式，在.css .js后面添加?v=n版本号, 以强制浏览器端刷新 '''
CONFIG_KEY = 'run_static_file_version_num'

def increaseVersionNum():
    curr_v = sh.getSiteConfig(CONFIG_KEY)
    next_v = int(curr_v) + 1 if curr_v else 0
    sh.setSiteConfig(CONFIG_KEY, next_v)

def appendVersionNum(handler):
    res = handler()
    html = sh.unicodeToStr(res) if isinstance(res, unicode) else str(res) 
    curr_v = int(sh.getSiteConfig(CONFIG_KEY, 0))
    if curr_v:
        regex_strings = (
            (''' (?<=<link\ )([^>]*href=")([^":]*?)(\.css)(".*?>) ''', r'\1\2\3?v=%d\4' % curr_v),
            (''' (?<=<script\ )([^>]*src=")([^":]*?)(\.js)(".*?>) ''', r'\1\2\3?v=%d\4' % curr_v),
        )
        for pattern, replace in regex_strings:
            regex = re.compile(pattern, re.I | re.S | re.X)
            html = regex.sub(replace, html)
    return html

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] != 'inc':
        print 'Usage: python tool/file_version.py inc'
    else:
        increaseVersionNum()
