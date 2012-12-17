#coding=utf-8
import site_helper as sh
import web

class Insert:

    def POST(self, inputs=None):
        if not inputs: inputs = self.getInputs()
        self._insert(inputs)
        return sh.refresh()

    def getInputs(self):
        inputs = web.input(image_file={})
        inputs = self.__processImageFile(inputs)
        return inputs

    def _insert(self, inputs):
        assert(inputs.has_key('model_name'))
        assert(sh.session.is_login)
        assert not inputs.has_key('Userid'), '请勿显示指定Userid，以免作弊'
        inputs.Userid = sh.session.user_id
        return sh.model(inputs.model_name).insert(inputs)

    # 把图片数据改为zarkpy规定的格式
    def __processImageFile(self, inputs):
        if inputs.has_key('image_file'):
            image_file = inputs.image_file
            if isinstance(image_file, str) or not image_file.filename \
                or len(image_file.value) < 10 or not image_file.type.startswith('image/'):
                del inputs.image_file
            else:
                inputs.image_file = sh.storage({'filename':image_file.filename, 'value': image_file.value, 'imagetype': image_file.type.partition('/')[2]})
        return inputs
