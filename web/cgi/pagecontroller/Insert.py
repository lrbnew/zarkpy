#coding=utf-8
import site_helper as sh

class Insert:

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        self._insert(inputs)
        return sh.refresh()

    def _insert(self, inputs):
        assert(inputs.has_key('model_name'))
        assert(sh.session.is_login)
        assert not inputs.has_key('Userid'), '请勿显示指定Userid，以免作弊'
        inputs.Userid = sh.session.user_id
        return sh.model(inputs.model_name).insert(inputs)

