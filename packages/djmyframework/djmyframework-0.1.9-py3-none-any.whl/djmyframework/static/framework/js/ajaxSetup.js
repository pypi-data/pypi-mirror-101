/*
ajax默认设置
 */


var csrftoken = getCookie('csrftoken');

//定义不需要csrftoken的请求方式
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//将csrftoken写入当前请求头
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },
    error: function (jqXHR, textStatus, errorMsg) {
        errorMsg += jqXHR.responseJSON ? jqXHR.responseJSON.msg : ''
        errorMsg = '发送AJAX请求到: "' + this.url + '" 时出错 <br>:[' + jqXHR.status + ']：<br>' + errorMsg

        art.dialog({id:errorMsg}).content(errorMsg);
    },
    //param 方法将会通过深度递归的方式序列化对象，以便符合现代化脚本语言的需求，比如 PHP、Ruby on Rails 等。你可以通过设置 jQuery.ajaxSettings.traditional = true; 来全局地禁用这个功能。
    traditional: true
});
