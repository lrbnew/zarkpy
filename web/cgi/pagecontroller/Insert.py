#coding=utf-8
import site_helper as sh
import web

class Insert:

    def POST(self, inputs=None):
        inputs = self.initInputs(inputs)
        assert(inputs.has_key('model_name'))
        assert(sh.session.is_login)
        model = sh.model(inputs.model_name)
        new_id = model.insert(inputs)
        return sh.refresh()

    def initInputs(self, inputs=None):
        if inputs is None:
            inputs = web.input(image_file={})

        # 把图片数据改为zarkpy规定的格式
        if inputs.has_key('image_file'):
            image_file = inputs.image_file
            if not image_file.filename or len(image_file.value) < 10 or not image_file.type.startswith('image/'):
                del inputs.image_file
            else:
                inputs.image_file = sh.storage({'filename':image_file.filename, 'value': image_file.value, 'imagetype': image_file.type.partition('/')[2]})

        inputs.Userid = sh.session.user_id
        inputs.ip     = sh.session.ip
        return inputs

    def GET(self):
        return self.POST()
