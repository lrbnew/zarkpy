#coding=utf-8
import site_helper as sh

class Insert:

    def GET(self, inputs=None):
        return self.POST(inputs)

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        return sh.toJsonp({'success':True, 'new_id': self._insert(inputs)})

    def _insert(self, inputs):
        assert inputs.has_key('model_name'), u'请指明需要插入的数据类型'
        assert sh.session.is_login, u'请先登录'
        inputs.Userid = sh.session.id
        return sh.model(inputs.model_name).insert(inputs)
