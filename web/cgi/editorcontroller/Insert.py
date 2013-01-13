#coding=utf-8
import web
import site_helper as sh

class Insert:

    def POST(self,inputs=None):
        self._insert(inputs)
        return sh.refresh()

    def _insert(self, inputs=None):
        if inputs is None: inputs = sh.inputs()
        assert(inputs.has_key('model_name'))
        return sh.model(inputs.model_name).insert(inputs)
