#coding=utf-8
import site_helper as sh

class User:
    model_name = 'User'

    def validate(self, email, password):
        user = sh.model(self.model_name).getOneByWhere('email=%s', [email.strip().lower()])
        return user and self.__validatePassword(user.password, password)

    def login(self, user, remember_me=False):
        sh.session.id = user.id
        sh.session.is_login = True
        sh.session.name = user.name
        if remember_me:
            sh.setCookie('email', user.email)
            sh.setCookie('md5password', user.password)
        if user.has_key('login_count'):
            sh.model(self.model_name).update(user.id, {'login_count': user.login_count+1})
        
    def logout(self):
        sh.session.id = 0
        sh.session.is_login = False
        sh.session.name = ''
        sh.setCookie('email',  '')
        sh.setCookie('md5password',  '')

    def __validatePassword(self, md5_password, text_password):
        return sh.model(self.model_name).getMD5Password(text_password) == md5_password
