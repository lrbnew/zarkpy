#coding=utf-8
import web
import site_helper as sh

class Delete:

    def POST(self,inputs=None):
        if inputs is None: inputs = sh.inputs()
        assert(inputs.has_key('model_name'))
        assert(inputs.has_key('model_id'))
        assert(sh.session.is_admin)
        model = sh.model(inputs.model_name)
        model.delete(int(inputs.model_id))
        return sh.refresh()
