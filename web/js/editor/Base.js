//===============refuse ie6================
if (navigator.userAgent.indexOf('MSIE') !== -1) {
    window.location.href = '/html/ieerror.html';
};

$(function(){
    // 去掉所有input的autocomplete, 显示指定的除外
    $('input:not([autocomplete]), textarea:not([autocomplete]), select:not([autocomplete])').attr('autocomplete', 'off');
});
