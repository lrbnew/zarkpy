#coding=utf-8
import site_helper as sh
# ../editor/ApiIndex.html

class ApiIndex:

    def GET(self):
        return sh.editor.ApiIndex(sh.model('APIDoc').all())
