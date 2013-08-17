#coding=utf-8
import imghdr
import site_helper as sh

class UserImage:

    def GET(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        assert inputs.has_key('action')
        model = sh.model('UserImage')
        
        if inputs.action in ['delete', 'recover']:
            assert sh.session.is_login
            assert inputs.get('UserImageid', None)
            exists = model.get(inputs.UserImageid)
            assert exists and exists.Userid == sh.session.id

            if inputs.action == 'delete':
                if sh.inModifyTime(exists.created):
                    model.delete(inputs.UserImageid)
                    return sh.toJsonp({'success': True})
                else:
                    return sh.toJsonp({'success': False, 'error': '超过了修改时限'})

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        assert inputs.has_key('action')

        if inputs.action == 'postImage':
            assert inputs.get('Userid', 0)
            assert sh.model('User').get(inputs.Userid)
            assert inputs.get('data_name', None)
            assert inputs.get('data_id', None)
            img_model = sh.model('UserImage')

            image_data = sh.getSwfUploadImageFile()

            new_id = img_model.insert(sh.storage(dict(image_file=image_data,
                Userid=inputs.Userid, file_name=image_data.filename,
                data_name=inputs.data_name, data_id=inputs.data_id)))

            return 'success;%d;%s;%s' % (new_id,
                    img_model.getUrlByPrivate(inputs.Userid, new_id), image_data.filename)
