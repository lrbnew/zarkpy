#coding=utf-8
import re
import time
import site_helper as sh

class User:
    model_name = 'User'

    # 验证密码是否正确
    def validate(self, email, password):
        user = sh.model(self.model_name).getOneByWhere('email=%s', [email.strip().lower()])
        return user and self.__validatePassword(user.password, password)

    def login(self, user, remember_me=False, ignore_cookie=False, inc_count=True):
        sh.session.id = user.id
        sh.session.is_login = True
        sh.session.name = user.name
        if remember_me and not ignore_cookie:
            sh.setCookie('email', user.email)
            sh.setCookie('md5password', user.password)
        if user.has_key('login_count') and inc_count:
            sh.model(self.model_name).update(user.id, {'login_count': user.login_count+1})

    def loginById(self, user_id, remember_me=False):
        user = sh.model(self.model_name).get(user_id)
        assert(user is not None)
        sh.ctrl(self.model_name).login(user, remember_me)
        
    def logout(self, ignore_cookie=False):
        sh.session.id = 0
        sh.session.is_login = False
        sh.session.name = ''
        if not ignore_cookie:
            sh.setCookie('email',  None)
            sh.setCookie('md5password',  None)

    # 向用户发送带有验证码的激活邮件
    def sendValidationEmail(self, user):
        code = self.__getValidationCode(user)
        sh.model('UserValidation').replaceInsert(dict(Userid=user.id, code=code))
        mail_text = '欢迎%s\n请点击激活: %s/accounts/validate?Userid=%d&code=%s' % (user.name, sh.config.HOST_NAME, user.id, code)
        sh.sendMail(user.email, '欢迎注册，请验证', mail_text)

    # 向用户发送重置密码的验证邮件
    def sendForgetPasswordEmail(self, user):
        code = self.__getValidationCode(user)
        sh.model('UserForgetPassword').replaceInsert(dict(Userid=user.id, code=code))
        mail_text = '%s您好，请申请了密码重置,此链接将在24小时后过期\n%s/accounts/forget-password?Userid=%d&code=%s\n若非您本人操作，请忽略本邮件' % (user.name, sh.config.HOST_NAME, user.id, code)
        sh.sendMail(user.email, '重置您的密码', mail_text)

    # 检查新注册的用户数据是否正确，不正确时返回错误信息
    def checkNewUser(self, data):
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        password = data.get('password', '')
        model = sh.model(self.model_name)

        if not re.match(r"^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$", email):
            return '请输入正确的邮箱地址'

        if model.getByEmail(email):
            return '此邮箱已注册'

        if model.getByName(name):
            return '此用户名已注册'

        if not (4 <= len(name) <=30):
            return '用户名必须大于等于4个字符，小于等于30个字符'

        if not(6 <= len(password) <= 60):
            return '密码必须大于等于6个字符，小于等于60个字符'

        # 限制用户名字符
        #if not re.match(r'^[a-zA-Z0-9_]+$', data.name.encode('utf-8')):
        #    return '用户名只能使用字母、数字、下划线'

        return None

    def register(self, data):
        data.register_ip = sh.session.ip
        return sh.model(self.model_name).insert(data)

    def __getValidationCode(self, user):
        return sh.toMD5(str(user.id) + str(time.time()))

    def __validatePassword(self, md5_password, text_password):
        return sh.model(self.model_name).getMD5Password(text_password) == md5_password
