#coding=utf-8
import site_helper as sh

class Profile:

    def POST(self):
        inputs = sh.inputs()

        if inputs['action'] == 'islogin':
            if sh.session.is_login:
                return sh.toJsonp({'is_login': True, 'name': sh.session.name, 'id': sh.session.id})
            else:
                return sh.toJsonp({'is_login': False, 'name': '', 'id': 0})

        if inputs['action'] == 'login':
            assert(inputs.get('email', '').strip())
            assert(inputs.get('password', ''))

            model = sh.model('User')
            uc = sh.ctrl('User')

            if not uc.validate(inputs.email, inputs.password):
                return sh.toJsonp({'is_login':False, 'error':'邮箱或密码不对'})

            user = model.getByEmail(inputs.email)

            if user.dead == 'yes':
                return sh.toJsonp({'is_login':False, 'error':'你已被列入黑名单'})

            uc.login(user, inputs.get('remember_me', '') == 'on')

            return sh.toJsonp({'is_login':True, 'name': user.name, 'id': user.id})

        if inputs['action'] == 'logout':
            sh.ctrl('User').logout()
            return 'bye'
