#coding=utf-8
import web
import site_helper as sh

# ../page/Alert.html

class Alert:

    def GET(self):
        inputs = web.input()
        return sh.page.Alert(inputs.get('msg'), inputs.get('referer'), inputs.get('stay'))
