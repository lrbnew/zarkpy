#coding=utf-8
import site_helper as sh
from User import User

class AdminUser(User):
    model_name = 'AdminUser'

    # 不能remember管理员，小心被盗号
    def login(self, user, remember_me=False):
        sh.session.admin_id = user.id
        sh.session.is_admin = True
        sh.session.admin_name = user.name
        
    def logout(self):
        sh.session.admin_id = 0
        sh.session.is_admin = False
        sh.session.admin_name = ''
        #del sh.session
