#coding=utf-8
import web, glob, sys, os
from urllib import quote as _quote, unquote as _unquote
import socket, struct
from urlparse import urlparse

# 程序的配置表. 注意文件夹路径必须以/结束
config = web.Storage({
    'APP_ROOT_PATH' :   '/opt/zarkpy/',
    'APP_PORT' :        10000,      # 程序运行的端口号，需与nginx配置的一致
    'SESSION_PATH' :    '/opt/zarkpy/session/', # session存放路径
    'COOKIE_EXPIRES' :  24 * 3600,  # cookie过期时间
    'SESSION_EXPIRES' : 24 * 3600,  # session过期时间
    # 程序异常log. 小心,如果有太多的error的话可能会导致写日志的死锁等待，导致程序响应慢
    'ERROR_LOG_PATH' :  '/opt/zarkpy/log/error.log',
    'FOOT_LOG_PATH' :   '',         # 访问程序的log, 一般情况下可以不使用
    'SECRET_KEY' :      'zarkpy',   # 程序密匙，每个新项目务必修改此key
    'HOST_NAME' :       'http://me.zarkpy.com',
})

# 初始化一些重要变量
web.config.session_parameters['timeout'] = config.SESSION_EXPIRES
web.config.session_parameters['secret_key'] = config.SECRET_KEY
session = None
page_render = None
page_render_nobase = None

def autoMkdir(path):
    path = path.rpartition('/')[0].strip()
    if path and not os.path.exists(path):
        print 'create dir:', path
        os.system('mkdir -p "%s"' % path)

# 获得一个文件夹下所有的module, 主要用于 __init__.py 文件中
def getDirModules(dir_path, dir_name, except_files=[]):
    assert(os.path.exists(dir_path))
    ret_modules = []
    for file_path in glob.glob(dir_path+'/*.py'):
        file_name = file_path.rpartition('/')[2].rpartition('.')[0]
        if file_name not in except_files:
            __import__(dir_name.strip('.')+'.'+file_name)
            if file_name in dir(getattr(sys.modules[dir_name.strip('.')],file_name)):
                ret_modules.append((file_name,getattr(getattr(sys.modules[dir_name.strip('.')],file_name),file_name)))
    return ret_modules

# 把整数ip转换为字符串
def ipToStr(ip_int):
    assert(isinstance(ip_int, int))
    return socket.inet_ntoa(struct.pack('=L', ip_int))

# 得到webpy提供的请求变量, 分别有:
# CONTENT_LENGTH CONTENT_TYPE DOCUMENT_ROOT HTTP_ACCEPT HTTP_ACCEPT_CHARSET HTTP_ACCEPT_ENCODING HTTP_ACCEPT_LANGUAGE HTTP_CONNECTION HTTP_COOKIE HTTP_HOST HTTP_REFERER HTTP_USER_AGENT PATH_INFO QUERY_STRING REMOTE_ADDR REMOTE_PORT REQUEST_METHOD REQUEST_URI SERVER_NAME SERVER_PORT SERVER_PROTOCOL
def getEnv(key):
    assert(isinstance(key, str))
    return web.ctx.env.get(key, '')

def quote(string):
    assert(type(string) in [unicode, str])
    return _quote(string.encode('utf-8')) if isinstance(string, unicode) else _quote(string)

def unquote(string):
    assert(type(string) in [unicode, str])
    return _unquote(string.encode('utf-8')) if isinstance(string, unicode) else _unquote(string)

# 得到url中的参数值，默认url为当前访问的url
def getUrlParams(url=None):
    if url is None:
        url = getEnv('REQUEST_URI')
    url = urlparse(url)
    return dict([(part.split('=')[0], _unquote(part.split('=')[1])) for part in url[4].split('&') if len(part.split('=')) == 2])

if __name__=='__main__':
    # 创建可能需要用到的文件夹，所以路径配置应该以_PATH结尾
    if len(sys.argv) == 2 and sys.argv[1] == 'init_dir':
        map(autoMkdir, [v for k,v in config.items() if k.endswith('_PATH')])
