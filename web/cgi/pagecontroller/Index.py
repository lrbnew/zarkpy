#coding=utf-8
import web
import site_helper as sh

# ../page/Index.html

class Index:

    def GET(self, cat=None):
        return sh.page_render.Index()
