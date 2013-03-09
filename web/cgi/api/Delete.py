#coding=utf-8
import site_helper as sh

class Delete:

    def GET(self, inputs=None):
        return self.POST(inputs)

    def POST(self,inputs=None):
        if not inputs: inputs = sh.inputs()
        assert inputs.has_key('model_name'), u'请指明需要修改的数据类型'
        assert inputs.has_key('model_id'),   u'请指明需要修改的数据id'

        model = sh.model(inputs.model_name)
        # 只允许删除自己的东西
        exists = model.get(inputs.model_id)
        if not exists:
            return sh.toJsonp({'success':True, 'affected': 0})

        if sh.session.is_login and exists.get('Userid', None) == int(sh.session.id):
            return sh.toJsonp({'success':True, 'affected': model.delete(inputs.model_id)})
        else:
            return sh.toJsonp({'success':False, 'msg':'不能删除不属于你的东西.'})
