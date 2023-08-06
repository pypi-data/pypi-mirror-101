/*
公用函数
 */

function getWindowHeightWidth() {
    if (window.innerWidth)
        winWidth = window.innerWidth;
    else if ((document.body) && (document.body.clientWidth))
        winWidth = document.body.clientWidth;
    // 获取窗口高度
    if (window.innerHeight)
        winHeight = window.innerHeight;
    else if ((document.body) && (document.body.clientHeight))
        winHeight = document.body.clientHeight;
    // 通过深入 Document 内部对 body 进行检测，获取窗口大小
    if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
        winHeight = document.documentElement.clientHeight;
        winWidth = document.documentElement.clientWidth;
    }
    return [winWidth, winHeight]
}

function stopEevent(e) {
    e.stopPropagation ? e.stopPropagation() : e.cancelBubble = true;
}

function setCookie(name, value) {
    var Days = 30;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
    document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// 时间类函数

//var s = "2006-12-13 09:41:30";
//var s2 = '2006-12-15 09:42:00';
function DateDiff(s, s2) {//sDate1和sDate2是2002-12-18格式
    var aDate, oDate1, oDate2, iDays;
    oDate1 = new Date(Date.parse(s.replace(/-/g, "/")));
    oDate2 = new Date(Date.parse(s2.replace(/-/g, "/")));

    iDays = parseInt(Math.abs(oDate1 - oDate2) / 1000 / 86399);
    if ((oDate1 - oDate2) < 0) {
        return -iDays;
    }
    return iDays;
}


/**
 * 得到日期年月日等加数字后的日期
 * @param interval  y    年
 q    季度
 m    月
 d    日
 w    周
 h    小时
 n    分钟
 s    秒
 ms    毫秒
 * @param number
 * @returns {Date}
 * @constructor
 */
Date.prototype.DateAdd = function (interval, number) {
    var d = this;
    var k = {
        'y': 'FullYear',
        'q': 'Month',
        'm': 'Month',
        'w': 'Date',
        'd': 'Date',
        'h': 'Hours',
        'n': 'Minutes',
        's': 'Seconds',
        'ms': 'MilliSeconds'
    };
    var n = {'q': 3, 'w': 7};
    eval('d.set' + k[interval] + '(d.get' + k[interval] + '()+' + ((n[interval] || 1) * number) + ')');
    return d;
}
/* 计算两日期相差的日期年月日等 */
Date.prototype.DateDiff = function (interval, objDate2) {

    var d = this, i = {}, t = d.getTime(), t2 = objDate2.getTime();
    i['y'] = objDate2.getFullYear() - d.getFullYear();
    i['q'] = i['y'] * 4 + Math.floor(objDate2.getMonth() / 4) - Math.floor(d.getMonth() / 4);
    i['m'] = i['y'] * 12 + objDate2.getMonth() - d.getMonth();
    i['ms'] = objDate2.getTime() - d.getTime();
    i['w'] = Math.floor((t2 + 345600000) / (604800000)) - Math.floor((t + 345600000) / (604800000));
    i['d'] = Math.floor(t2 / 86400000) - Math.floor(t / 86400000);
    i['h'] = Math.floor(t2 / 3600000) - Math.floor(t / 3600000);
    i['n'] = Math.floor(t2 / 60000) - Math.floor(t / 60000);
    i['s'] = Math.floor(t2 / 1000) - Math.floor(t / 1000);
    return i[interval];
}

// 对Date的扩展，将 Date 转化为指定格式的String
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
// 例子：
// (new Date()).Format("yyyy-MM-dd hh:mm:ss") ==> 2006-07-02 08:09:04.423
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
Date.prototype.Format = function (fmt) { //author: meizz
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}


function timestampFormat(timestamp, format) {
    var that = new Date(timestamp * 1000);
    var o = {
        "M+": that.getMonth() + 1, //month
        "d+": that.getDate(), //day
        "h+": that.getHours(), //hour
        "m+": that.getMinutes(), //minute
        "s+": that.getSeconds(), //second
        "q+": Math.floor((that.getMonth() + 3) / 3), //quarter
        "S": that.getMilliseconds() //millisecond
    }
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
        (that.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o) if (new RegExp("(" + k + ")").test(format))
        format = format.replace(RegExp.$1,
            RegExp.$1.length == 1 ? o[k] :
                ("00" + o[k]).substr(("" + o[k]).length));
    return format;
}

var timestamp_format = timestampFormat


function timestampToDatetimeStr(timestamp) {
    return timestampFormat(timestamp, 'yyyy-MM-dd hh:mm:ss')

}

var timestamp_to_datetime_str = timestampToDatetimeStr


function GetDatetimeStr(AddDayCount) {
    var timestamp = new Date().getTime() / 1000
    return timestamp_to_datetime_str(timestamp)
}

function datetimeStrToTimestamp(s) {
    return Date.parse(s.replace(/-/g, "/")) / 1000;
}

var datetime_str_to_timestamp = datetimeStrToTimestamp


/*   datetime_str:'2013-08-22 17:43:24' ,  604800  */
function addSecondsReturnTimestamp(datetime_str, seconds) {
    var t = datetime_str_to_timestamp(datetime_str) + seconds;
    return t;
}

//hh:ss转秒数
function timeStrToSec(sDate_str) {
    var time_and_min = sDate_str.split(':')
    return parseInt(time_and_min[0]) * 3600 + parseInt(time_and_min[1]) * 60
}

var time_str_to_sec = timeStrToSec

//秒数转hh:ss
function secToTimeStr(iTimeSec) {
    iTimeSec = parseInt(iTimeSec)
    var hours = parseInt(iTimeSec / 3600)
    var min = parseInt((iTimeSec % 3600) / 60)
    hours = hours < 10 ? '0' + hours : hours
    min = min < 10 ? '0' + min : min
    return hours + ':' + min
}

var sec_to_time_str = secToTimeStr

//短时间，形如 (13:04:06)
function isTime(str) {
    var a = str.match(/^(\d{1,2})(:)?(\d{1,2})\2(\d{1,2})$/);
    if (a == null) {
        return false;
    }
    if (a[1] > 24 || a[3] > 60 || a[4] > 60) {
        return false
    }
    return true;
}

//短日期，形如 (2008-07-22)
function strDate(str) {
    var r = str.match(/^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2})$/);
    if (r == null) return false;
    var d = new Date(r[1], r[3] - 1, r[4]);
    return (d.getFullYear() == r[1] && (d.getMonth() + 1) == r[3] && d.getDate() == r[4]);
}

//长时间，形如 (2008-07-22 13:04:06)
function strDateTime(str) {
    var reg = /^(\d{1,4})(-|\/)(\d{1,2})\2(\d{1,2}) (\d{1,2}):(\d{1,2}):(\d{1,2})$/;
    var r = str.match(reg);
    if (r == null) return false;
    var d = new Date(r[1], r[3] - 1, r[4], r[5], r[6], r[7]);
    return (d.getFullYear() == r[1] && (d.getMonth() + 1) == r[3] && d.getDate() == r[4] && d.getHours() == r[5] && d.getMinutes() == r[6] && d.getSeconds() == r[7]);
}


function getDatetimeFunc(str) {
    if (isTime(str)) return isTime
    if (strDate(str)) return strDate
    if (strDateTime(str)) return strDateTime
}

var get_datetime_func = getDatetimeFunc

function getDateStr(AddDayCount, is_edate) {
    var dd = new Date();
    var new_date = dd.dateAdd('d', AddDayCount)
    if (is_edate) {
        return new_date.Format("yyyy-MM-dd 23:59:59")
    }
    return new_date.Format("yyyy-MM-dd 00:00:00")
}


function getQueryParamMap() {
    var query_str = decodeURI(window.location.search.substring(1));
    var params = {}

    query_str.split('&').forEach(function (param) {
        var arr = param.split('=');
        if (arr[0]) {
            if (!params.hasOwnProperty(arr[0])) {
                params[arr[0]] = []
            }
            params[arr[0]].push(arr[1])
        }
    });
    return params

}

function linebreaksbr(str) {
    return str.toString().replace(/\n/g, '<br>')
}

jQuery.fn.outerHTML = function (s) {
    return (s) ? this.before(s).remove() : $("<Hill_man>").append(this.eq(0).clone()).html();
}

// 本地json数据
var localJson = {
    get: function (key, default_obj) {
        var json_str = localStorage.getItem(key)
        return json_str ? $.parseJSON(json_str) : default_obj
    },
    save: function (key, obj) {
        var json_str = ''
        if (typeof obj == 'object') {
            json_str = JSON.stringify(obj)
        }
        localStorage.setItem(key, json_str)
    },
    additem: function (key, item) {
        var item_list = this.get(key)
        item_list = $.isArray(item_list) ? item_list : []
        item_list.push(item)
        this.save(key, item_list)
    }
}


var QueryParamsMap = getQueryParamMap()
var browser = {
    versions: function () {
        var u = navigator.userAgent, app = navigator.appVersion;
        return {//移动终端浏览器版本信息
            trident: u.indexOf('Trident') > -1, //IE内核
            presto: u.indexOf('Presto') > -1, //opera内核
            webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核
            gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1, //火狐内核
            mobile: !!u.match(/AppleWebKit.*Mobile.*/), //是否为移动终端
            ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
            android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1, //android终端或者uc浏览器
            iPhone: u.indexOf('iPhone') > -1, //是否为iPhone或者QQHD浏览器
            iPad: u.indexOf('iPad') > -1, //是否iPad
            webApp: u.indexOf('Safari') == -1, //是否web应该程序，没有头部与底部
            weixin: u.indexOf('MicroMessenger') > -1, //是否微信
            qq: u.match(/\sQQ/i) == " qq" //是否QQ
        };
    }(),
    language: (navigator.browserLanguage || navigator.language).toLowerCase()
}


/*
导出excel
 tableToExcel('channel_table', 'W3C Example Table')
*/
var tableToExcel = (function () {
    var uri = 'data:application/vnd.ms-excel;base64,'
        ,
        template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>'
        , base64 = function (s) {
            return window.btoa(unescape(encodeURIComponent(s)))
        }
        , format = function (s, c) {
            return s.replace(/{(\w+)}/g, function (m, p) {
                return c[p];
            })
        }
    return function (table, name) {
        if (!table.nodeType) table = document.getElementById(table)
        var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML.replace(/height:[\W]?0px/g, '')}
        console.dir(table.innerHTML.replace(/height:[\W]?0px/, ''))
        window.location.href = uri + base64(format(template, ctx))
    }
})()


function ListTreeChildren(srcList, idKeyName, parentKeyName) {

    var idKeyName = idKeyName ? idKeyName : 'id'
    var parentKeyName = parentKeyName ? parentKeyName : 'parentId'
    var nodeInfo = srcList.reduce((data, node) => (data[node[idKeyName]] = node, data), {})

    // parent 列表转 tree
    this.toTree = function (handler) {
        let result = [];
        srcList.forEach(_node => {
            let node = handler ? handler(_node) : _node
            let parentKey = node[parentKeyName]
            if (!parentKey) {
                result.push(node)
                return
            }
            let parent = nodeInfo[parentKey]
            if (!parent) {
                alert(parentKey)
                return
            }
            parent.children = parent.children || []
            parent.children.push(node)
        })
        return result
    }

    // 增加 列表数 深度
    this.setLevel = function () {
        function getLevel(node) {
            var level = 0;
            if (nodeInfo[node[parentKeyName]]) {
                level += 1

                return level + getLevel(nodeInfo[node[parentKeyName]])
            }
            return level
        }

        srcList.forEach(node => {
            node.level = getLevel(node)
        })
        return srcList
    }

}

function customDispatchEvent(eventName, detail, isNoticeParent) {
    window.dispatchEvent(new CustomEvent(eventName, {detail: detail}))
    if (isNoticeParent) {
        window.parent.dispatchEvent(new CustomEvent(eventName, {detail: detail}))
    }

}