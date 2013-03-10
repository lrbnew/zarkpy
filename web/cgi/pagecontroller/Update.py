#coding=utf-8
import site_helper as sh

class Update:

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        self._update(inputs)
        return sh.refresh()

    def _update(self, inputs):
        assert inputs.has_key('model_name'), u'请指明需要修改的数据类型'
        assert inputs.has_key('model_id'),   u'请指明需要修改的数据id'
        assert sh.session.is_login, '请先登录'
        model = sh.model(inputs.model_name)
        exists = model.get(inputs.model_id)
        if exists is not None:
            assert exists.get('Userid', 0) == sh.session.id, u'您不能修改别人的数据'
            return model.update(inputs.model_id, inputs)
        else:
            return 0
