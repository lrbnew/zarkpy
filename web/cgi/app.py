#!/usr/bin/env python
#coding=utf-8
print 'starting app'
import web
import os
import datetime
from tool import nginx_uwsgi # nginx_uwsgi负责app.py和nginx之间的通信
import site_helper as sh # 注意，和shell没有关系, 只是一个简写而已:)
import pagecontroller

# debug模式默认为True，你可以在开发中设置为True，在发布中设置为False
# 当debug为True时, 网页的打开速度可能会很慢
# 当debug为False时，修改模版后必须重启程序才生效
#web.config.debug = False

urls = (
'/cgi/index','pagecontroller.Index', # pagecontroller/Index.py
'/cgi/insert','pagecontroller.Insert', # pagecontroller/Insert.py
'/cgi/update','pagecontroller.Update', # pagecontroller/Update.py
'/cgi/delete','pagecontroller.Delete', # pagecontroller/Delete.py
'/cgi/login','pagecontroller.user.Login', # pagecontroller/user/Login.py
'/cgi/logout','pagecontroller.user.Login', # pagecontroller/user/Login.py
'/cgi/register','pagecontroller.user.Register', # pagecontroller/user/Register.py
'/cgi/accounts/validate','pagecontroller.user.Validate', # pagecontroller/user/Validate.py
'/cgi/accounts/forget-password','pagecontroller.user.ForgetPassword', # pagecontroller/user/ForgetPassword.py
)

# init app
app = web.application(urls)

sh.session = web.session.Session(app, web.session.DiskStore(sh.config.SESSION_PATH), initializer={})

# 模版文件中可以直接访问的变量
template_enabled = {
    'str':          str,
    'int':          int,
    'len':          len,
    'type':         type,
    'map':          map,
    'all':          all,
    'any':          any,
    'hasattr':      hasattr,
    'getattr':      getattr,
    'input':        web.input,
    'sh':           sh,
    'session':      sh.session,
    'datetime':     datetime.datetime,
}

page_render_path = sh.config.APP_ROOT_PATH + 'web/cgi/page'
sh.autoMkdir(page_render_path)
sh.page = web.template.render(loc=page_render_path, base='Base', globals=template_enabled)
sh.page_nobase = web.template.render(loc=page_render_path, globals=template_enabled)

if __name__ == "__main__":
    from tool import init_database
    init_database.initTables()
    init_database.initDatas()
    print 'ok'
    app.run()
