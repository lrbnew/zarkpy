#coding=utf-8
# ../page/Index.html
import site_helper as sh

class Index:

    def GET(self):
        return sh.page.Index(sh.storage(locals()))
