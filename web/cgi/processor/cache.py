#coding=utf-8
import time, web, re, site_helper as sh
import hashlib

DEBUG = False
if sh.config.HOST_NAME != 'http://me.homework.com':
    import memcache
    mem_client = memcache.Client(['127.0.0.1:11211'], debug=0)

def cacheData(key, html, etag, retention=0, ):
    html = str(html)
    set_value = {'html': html, 'last_cached_time': time.time(), 'etag': etag }
    mem_client.set(key, set_value, retention)

def getData(key):
    data = mem_client.get(key)
    return data if data and data.has_key('html') else None

def getLastCachedTime(key):
    data = mem_client.get(key)
    return data['last_cached_time'] if data and data.has_key('last_cached_time') else 0

def getMD5(html):
    md5 = hashlib.md5()
    md5.update(html)
    return md5.hexdigest()

def cachePage(handler):
    if sh.getSiteConfig('run_use_cache') != 'yes': return handler()

    key = str(sh.getEnv('HTTP_HOST')) + sh.getEnv('REQUEST_URI')
    method = sh.getEnv('REQUEST_METHOD')
    retention = getCacheRetention()
    now = time.time()

    if method == 'GET' and sh.getEnv('HTTP_HOST') != sh.config.HOST_NAME:
        # 如果处于缓存有效期
        data = getData(key)
        if (now - getLastCachedTime(key) < retention) and data:
            html = data['html']
            # 设置charset=utf-8，否则nginx不使用gzip压缩
            web.header('Content-Type', 'text/html; charset=utf-8')
            # 设置etag头，有利益客户端缓存
            web.header('Etag', data['etag'])
            if DEBUG: print 'get cache'
        else:
            html = handler()
            if retention > 0:
                etag = getMD5(str(html))
                cacheData(key, html, etag, int(retention), )
                web.header('Etag', etag)
                if DEBUG: print 'set cache'
            else:
                if DEBUG: print 'retention == 0'
                pass
    else: # POST 与admin 请求不缓存
        if DEBUG: print 'post no cache'
        html = handler()

    return html

def getCacheRetention():
    return 20

def clear(key):
    mem_client.delete(key)
