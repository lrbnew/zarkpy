#coding=utf-8
import web
import site_helper as sh

# ../editor/Index.html

class Index:

    def GET(self):
        return sh.editor.Index()
