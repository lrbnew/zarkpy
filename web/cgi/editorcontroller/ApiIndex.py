#coding=utf-8
# ../editor/ApiIndex.html
import site_helper as sh

class ApiIndex:

    def GET(self):
        return sh.editor.ApiIndex(sh.model('APIDoc').all())
