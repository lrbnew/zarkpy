#coding=utf-8
import site_helper as sh

# ../page/Index.html

class Index:

    def GET(self):
        return sh.page.Index(sh.storage(locals()))
