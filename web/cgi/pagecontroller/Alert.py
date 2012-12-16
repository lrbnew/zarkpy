#coding=utf-8
import web
import site_helper as sh

# ../page/Alert.html

class Alert:

    def GET(self):
        inputs = web.input()
        msg = inputs.get('msg', '')
        referer = inputs.get('referer', '')
        stay = inputs.get('stay', 3)
        return sh.page.Alert(msg, referer)
