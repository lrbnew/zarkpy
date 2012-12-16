#coding=utf-8
import web
import site_helper as sh

# ../page/Index.html

class Index:

    def GET(self):
        bm = sh.model('Book')
        books = bm.all()
        p = bm.getPaginationHtml()
        return sh.page.Index(sh.storage(locals()))
