#coding=utf-8
import web
import site_helper as sh

def appendHeader(handler):
    request_path = sh.getEnv('REQUEST_URI').partition('?')[0]
    if request_path.startswith('/api/'):
        web.header('Content-Type', 'text/plain; charset=utf-8')
    return handler()
