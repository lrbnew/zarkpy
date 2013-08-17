#coding=utf-8
import site_helper as sh

class Update:

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        self._update(inputs)
        return sh.refresh()

    def _update(self, inputs):
        assert inputs.has_key('model_name')
        assert inputs.has_key('model_id')
        assert sh.session.is_login
        model = sh.model(inputs.model_name)
        exists = model.get(inputs.model_id)
        if exists is not None:
            assert exists.get('Userid', 0) == sh.session.id
            return model.update(inputs.model_id, inputs)
        else:
            return 0
