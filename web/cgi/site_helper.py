#coding=utf-8
import web, glob, sys, os, copy as _copy, hashlib, subprocess, json
from urllib import quote as _quote, unquote as _unquote
import socket, struct
from urlparse import urlparse

# 程序的配置表. 注意文件夹路径必须以/结束
config = web.Storage({
    'APP_ROOT_PATH' :   '/opt/zarkpy/',
    'APP_PORT' :        10000,      # 程序运行的端口号，需与nginx配置的一致
    'SESSION_PATH' :    '/opt/zarkpy/session/', # session存放路径
    'COOKIE_EXPIRES' :  7 * 24 * 3600,  # cookie过期时间
    'SESSION_EXPIRES' : 24 * 3600,  # session过期时间
    'DB_HOST' : '127.0.0.1',  # mysql数据库host
    'DB_DATABASE' : 'zarkpy', # mysql数据库名称
    'DB_USER' : 'zarkpy',     # mysql数据库用户名
    'DB_PASSWORD' : 'zarkpy_db_password', # mysql数据库连接密码
    'DB_TIMEOUT' : 800 * 3600,   # 连接超时时间, 默认800小时
    'DB_CHARSET' : 'utf8',
    'UPLOAD_IMAGE_PATH' : '/opt/zarkpy/web/img/upload/', # 其它上传图片存放目录
    'UPLOAD_IMAGE_URL'  : '/img/upload/', # 访问其它上传图片的相对路径
    # 程序异常log,小心,如果有太多的error的话可能会导致写日志的死锁等待,导致程序响应慢
    'ERROR_LOG_PATH' :  '/opt/zarkpy/log/error.log',
    'FOOT_LOG_PATH' :   '',   # 访问log, 一般情况下可以不使用
    'SECRET_KEY' :      'zarkpy',   # 程序密匙,每个新项目务必修改此key
    'HOST_NAME' :       'http://me.zarkpy.com',
    'MAIL_SENDER' :     'noreply@zarkpy.com', # 邮件的默认发送者
    'IS_TEST' :       False, # 是否正在测试，测试时会被修改为True
})

# 初始化一些重要变量
web.config.session_parameters['timeout']    = config.SESSION_EXPIRES
web.config.session_parameters['secret_key'] = config.SECRET_KEY
session = None
page = None
page_nobase = None
module = None

# 根据path自动创建文件夹，使用此函数来避免抛出找不到文件夹的异常
def autoMkdir(path):
    path = path.rpartition('/')[0].strip()
    if path and not os.path.exists(path):
        print 'WARNING: auto create dir', path
        os.system('mkdir -p "%s"' % path)

# 获得一个文件夹下所有的module,主要用于__init__.py文件自动import所有class
def getDirModules(dir_path, dir_name, except_files=[]):
    assert(os.path.exists(dir_path))
    ret_modules = []
    for file_path in glob.glob(dir_path+'/*.py'):
        file_name = file_path.rpartition('/')[2].rpartition('.')[0]
        if file_name not in except_files:
            __import__(dir_name.strip('.') + '.' + file_name)
            if file_name in dir(getattr(sys.modules[dir_name.strip('.')], file_name)):
                ret_modules.append((file_name, getattr(getattr(sys.modules[dir_name.strip('.')], file_name), file_name)))
    return ret_modules

# 缓存model实例,因为一但model建立,在程序运行过程中是不会改变model的
CACHED_MODELS = {}
# model函数从model文件夹中找到名称为model_name的model
# 然后得到他的一个实例并用modeldecorator装饰后return
def model(model_name):
    cache_key = model_name

    if CACHED_MODELS.has_key(cache_key):
        return CACHED_MODELS[cache_key]
    else:
        # 此import语句不能放到model函数外面去
        # 否则会与model中的import site_helper语句形成互相依赖
        import model
        import modeldecorator 
        try:
            for name in model_name.split('.'):
                assert(hasattr(model, name))
                model = getattr(model, name)
            model = model()
        except:
            print 'the name is', name
            print 'the model name is', model_name
            raise
        for d,arguments in model.decorator:
            # 某些装饰器不用测试
            if not config.IS_TEST or getattr(modeldecorator, d).test_me:
                model = getattr(modeldecorator, d)(model, arguments)
        CACHED_MODELS[cache_key] = model
        return model

# 获得controller模块中的实例
def ctrl(name):
    import controller
    try:
        for name in name.split('.'):
            assert(hasattr(controller, name))
            controller = getattr(controller, name)
    except:
        print 'the name is', name
        print 'the controller name is', name
        raise
    return controller()

def getDBHelper():
    from model import DBHelper
    return DBHelper()

def ipToInt(ip_str):
    assert(isinstance(ip_str, str))
    return struct.unpack('=L',socket.inet_aton(ip_str))[0]

def ipToStr(ip_int):
    assert(isinstance(ip_int, int))
    return socket.inet_ntoa(struct.pack('=L', ip_int))

# 获得webpy提供的request变量, key的取值可以为:
# CONTENT_LENGTH CONTENT_TYPE DOCUMENT_ROOT HTTP_ACCEPT HTTP_ACCEPT_CHARSET HTTP_ACCEPT_ENCODING HTTP_ACCEPT_LANGUAGE HTTP_CONNECTION HTTP_COOKIE HTTP_HOST HTTP_REFERER HTTP_USER_AGENT PATH_INFO QUERY_STRING REMOTE_ADDR REMOTE_PORT REQUEST_METHOD REQUEST_URI SERVER_NAME SERVER_PORT SERVER_PROTOCOL
def getEnv(key, default=''):
    assert(isinstance(key, str))
    return web.ctx.env.get(key, default)

def unicodeToStr(s):
    assert(type(s) in [unicode, str])
    return s.encode('utf-8', 'ignore') if isinstance(s, unicode) else s

def quote(*l):
    return tuple(_quote(unicodeToStr(s)) for s in l) if len(l) != 1 else _quote(unicodeToStr(l[0]))

def unquote(*l):
    return tuple(_unquote(unicodeToStr(s)) for s in l) if len(l) != 1 else _unquote(unicodeToStr(l[0]))

# 得到url中的参数值,默认url为当前访问的url
def getUrlParams(url=None):
    if url is None: url = getEnv('REQUEST_URI')
    url = urlparse(url)
    return dict([(part.split('=')[0], _unquote(part.split('=')[1])) for part in url[4].split('&') if len(part.split('=')) == 2])

# 把网络访问地址转为本地文件路径
def urlToPath(url):
    assert(url.startswith('/'))
    assert(not url.startswith(config.APP_ROOT_PATH + 'web'))
    return config.APP_ROOT_PATH + 'web' + url

# 把本地文件路径转为网络访问地址
def pathToUrl(path):
    assert(path.startswith(config.APP_ROOT_PATH + 'web' + '/'))
    return path.partition(config.APP_ROOT_PATH + 'web')[2]

# 打印一个dict或list的值，便于调试
def printDictOrList(d, index=0):
    if type(d) is dict or type(d) is web.Storage:
        for k, v in d.items():
            print ' ' * index + k, ':'
            printDictOrList(v, index+4)
    elif type(d) is list or type(d) is tuple:
        for i in d:
            printDictOrList(i, index+4)
    else:
        print ' ' * index + unicodeToStr(d)

# 返回一个可以用foo.abc代替foo['abc']的dict
def storage(data={}):
    return web.Storage(data)

def getSiteConfig(name, default=''):
    exists = model('SiteConfig').getOneByWhere('name=%s', [name])
    return exists.value.strip() if exists and exists.value.strip() else default

def setSiteConfig(name, value):
    model = model('SiteConfig')
    assert(name.strip())
    exists = model.getOneByWhere('name=%s', [name])
    if exists:
        model.update(exists.id, dict(value=value))
        return exists.id
    else:
        return model.insert(dict(name=name, value=value))

def getReferer(referer=None):
    if not referer:
        referer = web.input().get('referer', None)
    if not referer:
        referer = web.ctx.env.get('HTTP_REFERER', None)
        if referer and not referer.startswith(config.HOST_NAME):
            referer = None
    return referer

def toMD5(text):
    m = hashlib.md5()
    m.update(config.SECRET_KEY + unicodeToStr(text))
    return m.hexdigest()

# 刷新当前页面，可以通过referer参数指定打开的页面
def refresh(referer=None):
    referer = getReferer(referer)
    return web.seeother(referer if referer else '/')

# 跳转到/alert页面，显示一条消息，然后再跳转到另一个页面
def alert(msg, referer=None, stay=3):
    referer = getReferer(referer)
    if not referer: referer = '/'
    return web.seeother('/alert?msg=%s&referer=%s&stay=%s' % quote(msg, referer, str(stay)))

def redirect(url):
    web.seeother(url)

def redirectTo404():
    web.seeother('/404.html')

def redirectToLogin(referer=None):
    referer = getReferer(referer)
    url = '/login?referer=%s' % quote(referer if referer else '/')
    web.seeother(url)

def copy(obj):
    return _copy.deepcopy(obj)

def filterNone(l):
    return [i for i in l if i is not None]

# 设置浏览器cookie，value为None时删除cookie
def setCookie(key, value):
    if value is not None:
        web.setcookie(key, value, config.COOKIE_EXPIRES)
    else:
        web.setcookie(key, '', 0)

# 发送邮件，需要已设置exim4以及mail程序, 以及exim4.conf中的域名指向你的服务器ip
# 安装命令: sudo aptitude install exim4 heirloom-mailx
# 使用配置: cp /opt/zarkpy/conf/exim4.conf /etc/exim4/exim4.conf
#           sudo /etc/init.d/exim4 restart
# 发送命令: cat content_file | mail -s subject -r sender@domain.com -B receiver
def sendMail(email, subject, content, sender=None):
    if not sender: sender = config.MAIL_SENDER
    p = subprocess.Popen(['mail','-s',subject,'-r',sender,'-B',email],stdout=subprocess.PIPE,stdin=subprocess.PIPE)
    p.stdin.write(content)
    p.communicate()
    p.stdin.close()

def inputs():
    def __processImageFile(inputs):
        if inputs.has_key('image_file'):
            image_file = inputs.image_file
            if isinstance(image_file, str) or isinstance(image_file, dict) or not image_file.filename \
                or len(image_file.value) < 10 or not image_file.type.startswith('image/'):
                del inputs.image_file
            else:
                inputs.image_file = storage(dict(filename=image_file.filename, value=image_file.value, imagetype=image_file.type.partition('/')[2]))
        return inputs
    return __processImageFile(web.input(image_file={}))

def toJsonp(data):
    def __jsonEnabled(data):
        json_enable = [int, long, str, bool, list, dict, web.utils.Storage]
        if isinstance(data, dict) or isinstance(data, web.Storage):
            return dict([(k, __jsonEnabled(v)) for k,v in data.items()])
        elif isinstance(data, list) or isinstance(data, tuple):
            return list(__jsonEnabled(v) for v in data)
        elif type(data) in json_enable:
            return data
        else:
            return str(data)
    data = __jsonEnabled(data)
    cb = web.input().get('callback', None)
    return '%s(%s);' % (cb, json.dumps(data)) if cb else json.dumps(data)

def splitAndStrip(string, chars=' '):
    return [s.strip() for s in string.split(chars) if s.strip()]

if __name__=='__main__':
    # 创建可能需要用到的文件夹，所以路径配置应该以_PATH结尾
    if len(sys.argv) == 2 and sys.argv[1] == 'init_dir':
        map(autoMkdir, [v for k,v in config.items() if k.endswith('_PATH')])
