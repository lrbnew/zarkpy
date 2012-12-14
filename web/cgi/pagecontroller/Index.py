#coding=utf-8
import web
import site_helper as sh

# ../page/Index.html

class Index:

    def GET(self):
        return sh.page_render.Index(sh.storage(locals()))
