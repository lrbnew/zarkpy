#coding=utf-8
import site_helper as sh

class Delete:

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        self._delete(inputs)
        return sh.refresh()

    def _delete(self, inputs):
        assert inputs.has_key('model_name'), '请指明需要修改的数据类型'
        assert inputs.has_key('model_id'),   '请指明需要修改的数据id'
        assert sh.session.is_login, '请先登录'
        model = sh.model(inputs.model_name)
        exists = model.get(inputs.model_id)
        if exists is not None:
            assert exists.get('Userid', 0) == sh.session.id, '您不能删除别人的数据'
            return model.delete(inputs.model_id)
        else:
            return 0
