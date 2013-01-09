#coding=utf-8
import web
import site_helper as sh

class Update:

    def POST(self,inputs=None):
        self._update(inputs)
        return sh.refresh()

    def _update(self, inputs=None):
        assert(sh.session.is_admin)
        if inputs is None: inputs = sh.inputs()
        return sh.model(inputs.model_name).update(int(inputs.model_id),inputs)
