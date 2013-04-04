#coding=utf-8
import site_helper as sh

def printDict(handler):
    html = str(handler())
    # 此功能仅对后台管理员开放，以免影响正式调用api时的返回结果
    if sh.session.is_admin and html and html[0] == '{' and html[-1] == '}':
        html = sh.printObject(sh.loadsJson(html), not_user_column_names=True)
    return html
