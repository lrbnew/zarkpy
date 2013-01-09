#coding=utf-8
import web.net
from web.utils import Profile
import site_helper as sh

def profiler(handler):
    if sh.session.is_admin and sh.getUrlParams().get('profile', None):
        html, x = Profile(handler)()
        return str(html) + '<pre>' + str(web.net.websafe(x)) + '</pre>'
    else:
        return handler()
