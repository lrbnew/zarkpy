#coding=utf-8
import site_helper as sh

class Get:

    def GET(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        assert inputs.has_key('model_name'), u'请指明需要查询的数据类型'
        assert inputs.has_key('model_id'), u'请指明需要查询的数据id'
        item = sh.model(inputs.model_name).get(inputs.model_id)
        if item:
            item = dict(item)
            item['id'] = int(inputs.model_id)
        return sh.toJsonp(item)
