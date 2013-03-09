#coding=utf-8
# ../../api/Insert.py
import site_helper as sh

class Insert:

    def GET(self, inputs=None):
        return self.POST(inputs)

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        return self._insert(inputs)

    def _insert(self, inputs):
        assert inputs.has_key('model_name'), u'请指明需要插入的数据类型'
        if not sh.session.is_login:
            return sh.toJsonp({'success':False, 'error': '请先登录'})
        inputs.Userid = sh.session.id
        return sh.toJsonp({'success':True, 'new_id': sh.model(inputs.model_name).insert(inputs)})
