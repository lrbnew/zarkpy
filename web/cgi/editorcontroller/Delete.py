#coding=utf-8
import site_helper as sh

class Delete:

    def GET(self):
        return self.POST()

    def POST(self,inputs=None):
        self._delete(inputs)
        return sh.refresh()

    def _delete(self, inputs=None):
        assert(sh.session.is_admin)
        if inputs is None: inputs = sh.inputs()
        assert(inputs.has_key('model_name'))
        assert(inputs.has_key('model_id'))
        return sh.model(inputs.model_name).delete(int(inputs.model_id))
