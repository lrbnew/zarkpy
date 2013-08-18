//functions for ajax login
(function(){
    // 声明全局变量
    var namespace = 'sign';
    if (!window[namespace]) window[namespace] = {};
    var sign = window[namespace];

    // 选择器配置表
    var selector = {
        login_div       : '#sign_login_div', // 弹出的登录窗div
        login_error     : '#sign_login_error', // 登录错误的提示
        login_email     : '#sign_login_email', // 登录时输入email的input
        login_password  : '#sign_login_password', // 登录时输入密码的input
        login_remember  : '#sign_login_remember_me', // 是否记住我的input checkbox
        login_btn       : '#sign_login_btn', // 发起登录的按钮
        close_btn       : '#sign_close_btn', // 关闭登录弹窗的按钮
        overlayer       : '#sign_overlayer', // 弹窗遮罩层
        // 登录成功后的附加回调函数, 仅在用户主动登录后运行
        success         : function(name, Userid) {
            $('#login_name').html(name);
        }
    };

    // 输入验证正则
    var validate = {
        email: /^([.a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/,
        password: /.+/,
        name: /.+/
    };

    // 输入验证错误提示
    var error = {
        email: '请输入Email地址', 
        password: '请输入的密码',
        name: '请输入用户名'
    };

    var login_callback = null;

    // 当执行某个函数需要先确保用户已经登录时，就用requireLogin包一下
    // 如果用户没有登录，就会先弹出登录窗口，确保登录后再执行callback
    sign.requireLogin = function(callback){
        api.isLogin({callback:function(data){
            if (data.is_login) callback();
            else sign.pleaseLogin(callback);
        }});
    };

    // 弹出要求用户登录的窗口，登录成功后执行callback
    sign.pleaseLogin = function(callback){
        login_callback = callback;
        $(selector.overlayer).show();
        $(selector.login_div).fadeIn();
        $(selector.login_email).focus();
    };

    // 读取用户输入的数据, 发起login请求
    // 当用户成功登录后执行login_callback
    // 执行此函数前zark.isLogin()应该等于false
    sign.tryLogin = function(){
        var post_data = {
            email:      $.trim($(selector.login_email).val()),
            password:   $(selector.login_password).val(),
            remember_me:$(selector.login_remember).val()
        }
        // 验证输入
        for (var check in validate){
            if (!validate[check].test(post_data[check])){
                $(selector.login_error).html(error[check]).show();
                return false;
            };
        };
        $(selector.login_error).html('');
        sign.login(post_data, login_callback);
    };

    // 用email和password数据发起login请求
    sign.login = function(post_data, success_callback){
        post_data.callback = function(data){
            if (data.is_login){
                success_callback && success_callback();
                sign.unpleaseLogin(data.name, data.user_id);
                if ( selector.success ) {
                    selector.success(data.name, data.user_id);
                };
            }else{
                $(selector.login_error).html('用户名或密码不对').show();
            };
        };
        api.login(post_data);
    };

    // 关闭登录弹窗
    sign.unpleaseLogin = function(){
        $(selector.login_div).fadeOut('fast');
        $(selector.overlayer).fadeOut('fast');
    };

    // 绑定发起登录和取消登录的按钮事件
    $(function() {
        if ( selector.login_btn ) {
            $(selector.login_btn).click(sign.tryLogin);
        };
        if ( selector.close_btn ) {
            $(selector.close_btn).click(sign.unpleaseLogin);
        };
    })

})();
