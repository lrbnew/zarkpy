#coding=utf-8
import web.net, site_helper
from web.utils import Profile

def profiler(handler):
    if site_helper.session.is_admin and site_helper.getUrlParams().get('profile', None):
        html, x = Profile(handler)()
        return str(html) + '<pre>' + str(web.net.websafe(x)) + '</pre>'
    else:
        return handler()

