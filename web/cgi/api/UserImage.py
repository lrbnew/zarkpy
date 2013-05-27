#coding=utf-8
# ../subpage/ChooseImage.html
import site_helper as sh
import imghdr

class UserImage:

    def GET(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        assert inputs.has_key('action')
        model = sh.model('UserImage')
        
        # assert
        if inputs.action not in ['getChooseImageHtml']:
            assert sh.session.is_login
            assert inputs.get('UserImageid', None)
            exists = model.get(inputs.UserImageid)
            assert exists and exists.Userid == sh.session.id

        if inputs.action == 'getChooseImageHtml':
            assert sh.session.is_login
            env = dict(paging=False, where=['deleted=%s','no'])
            images = model.all(env)
            #paging = model.getPaginationHtml(env)
            paging = ''
            html = str(sh.subpage.ChooseImage(images, paging))
            return sh.toJsonp({'success': True, 'html': html, 'Userid': sh.session.id})

        elif inputs.action == 'delete':
            model.update(inputs.UserImageid, {'deleted': 'yes'})
            return sh.toJsonp({'success': True})

        elif inputs.action == 'realDelete':
            model.delete(inputs.UserImageid)
            return sh.toJsonp({'success': True})

        elif inputs.action == 'recover':
            model.update(inputs.UserImageid, {'deleted': 'no'})
            return sh.toJsonp({'success': True})

    def POST(self, inputs=None):
        if not inputs: inputs = sh.inputs()
        assert inputs.has_key('action')

        if inputs.action == 'postImage':
            assert inputs.get('Userid', 0)
            assert sh.model('User').get(inputs.Userid)
            img_model = sh.model('UserImage')
            image_type = imghdr.what(None, inputs['Filedata'])

            file_name = inputs['Filename'].partition('.')[0]
            if '.' in file_name:
                file_name = file_name.partition('.')[2]
            assert image_type in img_model.known_types

            image_data = sh.storage({'filename':file_name,
                'value':inputs['Filedata'], 'imagetype': image_type})

            new_id = img_model.insert(sh.storage(dict(image_file=image_data,
                Userid=inputs.Userid, file_name=file_name)))

            return 'success;%d;%s;%s' % (new_id,
                    img_model.getUrlByPrivate(inputs.Userid, new_id), file_name)
