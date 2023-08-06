/*
ui界面相关
 */

function initSelectTree() {
    //select2
    $(".select2-tree").each(function (i, ele) {
        var $ele = $(ele)
        var url = $(this).attr('data-url')
        var keyName = $(this).attr('data-keyName') || $(this).attr('data-key') || 'alias'
        var defaultVal = $ele.val()
        var parentKeyName = $(this).attr('data-parentKeyName') || 'parent'
        if ($(ele).attr('data-already-init')) {
            return
        }

        $.getJSON(url, {page_size: 1000, fields: 'id,name,alias,username,parent,parent_id'}, function (rsp) {
            $(ele).html('')
            $(ele).append('<option value="">*</option>')
            var data = rsp.data.results
            data = new ListTreeChildren(data, 'id', parentKeyName).setLevel()

            var results = $.map(data, function (row) {
                var text = row[keyName]
                if (row.level > 0) {
                    var placeholder = '&nbsp;&nbsp;&nbsp;'
                    text = placeholder.repeat(row.level) + '└─' + placeholder + text
                }
                var option_data = {id: row.id, text: text || row.alias, parent: row.parent ? row.parent : ''}

                $(ele).append('<option value="' + option_data.id + '" parent="' + option_data.parent + '">' + option_data.text + '</option>')
                return option_data
            })


            console.dir(data)
            $(ele).attr('data-already-init', 'true')

            $(ele).select2({
                width: '200px',
                placeholder: '请选择',
                language: BootstrapTableLocale,
                allowClear: true,
                theme: "bootstrap"
            })
            $(ele).val(defaultVal).trigger('change');
        })
    })

}


function initSelect2() {
    //select增加svalue为默认选择
    $("select[svalue]").each(function () {
        target = $(this);
        var value = target.attr('svalue');
        if (value == undefined) {
            return;
        }
        target.find('option').each(function () {
            o = $(this);
            if (value == o.val()) {
                o.attr('selected', true);
                return;
            }
        })
    });

    //select2
    $("select.select2").each(function (i, ele) {
        var $ele = $(ele)
        var url = $(this).attr('data-url')
        var keyName = $(this).attr('data-keyName') || $(this).attr('data-key') || 'alias'
        var defaultVal = $ele.val()
        if ($(ele).attr('data-already-init')) {
            return
        }

        if (url) {
            $.getJSON(url, {page_size: 1000, fields: 'id,name,alias,username'}, function (rsp) {
                var results = $.map(rsp.data.results, function (row) {
                    return {id: row.id, text: row[keyName] || row.alias}
                })
                // 添加默认 option 元素
                $ele.find('option').each(function (i, op) {
                    !op.selected ? results.unshift({id: op.value, text: op.innerText}) : null
                })
                $(ele).html('')
                console.dir(results)
                $(ele).attr('data-already-init', 'true')
                $(ele).select2({
                    data: results,
                    width: 'auto',
                    placeholder: '请选择',
                    language: BootstrapTableLocale,
                    allowClear: true,
                    theme: "bootstrap"
                })
                $(ele).val(defaultVal).trigger('change');
            })

        } else {
            $ele.select2({
                width: 'auto',
                placeholder: '请选择',
                language: BootstrapTableLocale,
                allowClear: $ele.attr('data-allow-clear') == 'true' ? true : false,
                theme: "bootstrap"
            })
        }
        $(ele).attr('data-already-init', 'true')

    })
}

// Vue select2 实现双向绑定
Vue ? Vue.directive('select2', {
    twoWay: true,
    inserted: function (el, binding, vnode) {

        $(el).on("change", function (e) {

            for (var i = 0; i < vnode.data.directives.length; i++) {
                if (vnode.data.directives[i].name == "model") {
                    var expression = vnode.data.directives[i].expression
                    var attrKeyDepth = expression.split('.')
                    var lastAttrName = attrKeyDepth.pop()
                    var attr = vnode.context
                    for (var i = 0; i < attrKeyDepth.length; i++) {
                        attr = attr[attrKeyDepth[i]]
                    }
                    attr[lastAttrName] = $(this).val()
                    // console.dir(e)
                    // console.dir(attr[lastAttrName])
                    // console.dir(attr)
                    break
                }
            }

        });
    },

    update: function (el, binding, vnode) {
        for (var i = 0; i < vnode.data.directives.length; i++) {
            if (vnode.data.directives[i].name == "model") {
                $(el).val(vnode.data.directives[i].value).trigger("change");
                break
            }
        }

    },
    unbind: function (el) {
        $(el).off().select2('destroy')
    }
}) : null;


function initTagsinput() {
    $('.tagsinput').tagsinput()
}


function enfoldment(id) {
    $('#' + id).toggleClass('enfoldment');
}

// 设置input值
function inputText(inputName, inputValue) {
    $("input[name='" + inputName + "']").val(inputValue);
}


// 异步刷新不跳转
function ajax_delete(ele, url) {
    var $ele = $(ele)
    var tr = $ele.is('tr') ? $ele : $ele.parents('tr').first()
    var del_url = url ? url : $ele.attr('href')
    $.ajax({
        url: del_url,
        type: 'POST'
    })
        .done(function (response, status, xhr) {
            if (xhr.status == 200) {
                tr.remove()
                art.dialog('删除成功').time(3)
            }

        })
        .fail(function (response, status, xhr) {
            alert('删除失败!')
            console.dir(response)
            console.dir(status)
            console.dir(xhr)
        })


}

/*jquery扩展 dialog*/
function myDialog(op, height) {
    //var _top = "45%"
    if (typeof op == "object") {
        if (top.location != self.location) {
            var __top = parent.document.documentElement.scrollTop || parent.document.body.scrollTop
            _top = parseInt(__top) + 100
            op = $.extend({"top": _top}, op);
        }


    } else {
        op = {"content": op, "fixed": true, top: "25%"}
    }
    console.dir(op)
    var _dialog = art.dialog(op)
    return _dialog
}

function closeALlDialog() {
    var list = art.dialog.list;
    for (var i in list) {
        list[i].close();
    }
}

function closeSelfDialog() {
    parent.artDialog.list[window.name] ? parent.artDialog.list[window.name].close() : null
}

(function ($) {
    $.fn.extend({
        /*dialog*/
        "dialog": function (op) {
            if ('close' == op) {
                //art.dialog.list[this.attr('id')].close()
                return
            }

            op = $.extend({
                content: this[0],
                id: $(this).attr('id'),
            }, op);
            return myDialog(op, $(this).height()).show()
        },
    });
})(jQuery);
$.dialog = myDialog

function alertError(msg) {
    msg = msg.replace(/\n/, '<br>')
    return art.dialog({
        id: msg, width: "50%"
    }).title('Alert').content('<div class="pre-scrollable alert alert-danger">' + msg + '</div>')
}

function alertMsg(msg) {
    return art.dialog({id: msg}).content(msg)
}

$(document).on('click', '.dialog', function (event) {
    event.preventDefault();
    var follow = $(this).attr('follow') ? this : false
    console.dir(follow)
    var _dialog = $.dialog({id: this.href, title: $(this).text(), follow: follow});
    $.ajax({
        url: this.href,
        success: function (data) {
            _dialog.content(data);
        },
        cache: false
    });

    //artDialog.load(this.href,{title: $(this).text()},false);
    return false

}).on('click', '.openDialog,opendialog', function (event) {
    event.preventDefault();
    var This = $(this)
    var url = This.attr('url') ? This.attr('url') : This.attr('href')
    var title = This.attr('title') ? This.attr('title') : This.text()
    var width = This.attr('data-width') ? This.attr('data-width') : "auto";
    var height = This.attr('data-height') ? This.attr('data-height') : "auto";

    art.dialog.open(url, {title: title, width: width, height: height, id: url})
    stopEevent(event)
    return false

}).on('click', '.openDialog1,opendialog1', function (event) {
    event.preventDefault();
    var This = $(this)
    var url = This.attr('url') ? This.attr('url') : This.attr('href')
    var width = This.attr('data-width') ? This.attr('data-width') : "";
    var height = This.attr('data-height') ? This.attr('data-height') : "1024px";


    var title = This.attr('title') ? This.attr('title') : This.text()
    art.dialog.open(url, {title: title, width: width, height: height})
    stopEevent(event)
    return false
}).on('click', '.ask-openDialog', function (event) {
    event.preventDefault();
    var This = $(this)
    if (!confirm("确认进行此操作吗 ?")) {
        return false
    }
    var url = This.attr('url') ? This.attr('url') : This.attr('href')
    var width = This.attr('data-width') ? This.attr('data-width') : "";
    var height = This.attr('data-height') ? This.attr('data-height') : "";

    var title = This.attr('title') ? This.attr('title') : This.text()
    art.dialog.open(url, {title: title, width: width, height: height})
    stopEevent(event)
    return false
}).on('click', '.popoverdialog,.popoverDialog,[data-toggle="popoverdialog"]', function (event) {
    event.preventDefault();
    var This = $(this)
    var dialog_id = This.attr('data-dialog-id')
    var tpl_el_id = This.attr('data-tpl-id')
    var tpl_data = This.attr('data-tpl-data')
    var title = This.attr('data-dialog-title') || ''
    var data_content = This.attr('data-content')
    if (data_content == undefined && tpl_el_id && tpl_data) {
        data_content = render_vue_tpl(tpl_el_id, JSON.parse(tpl_data))
    }
    art.dialog({
        id: dialog_id,
    }).title(title).content(data_content).follow(this);

    return false
})


/* POST打开新窗口
@url 地址
@name 窗口名
@fWidth 窗口宽系数 0.5 
@fHeight 窗口高系数 0.5
@Data POST 的数据 aa=aa&aa=bb
*/
function openwindow(url, name, fWidth, fHeight, Data) {
    var url;                                 //转向网页的地址;
    var name;                           //网页名称，可为空;
    var iWidth = parseInt(window.screen.availWidth * fWidth),                          //弹出窗口的宽度;
        iHeight = parseInt(window.screen.availHeight * fHeight)
    var iTop = parseInt((window.screen.availHeight - iHeight) / 2),      //获得窗口的垂直位置;
        iLeft = parseInt((window.screen.availWidth - iWidth) / 2);           //获得窗口的水平位置;

    var Window_obj = window.open(url, name, 'height=' + iHeight + ',,innerHeight=' + iHeight + ',width=' + iWidth + ',innerWidth=' + iWidth + ',top=' + iTop + ',left=' + iLeft + ',scrollbars=yes');
    //,toolbar=no,menubar=no,scrollbars=yes,resizeable=no,location=no,status=no');
    if (Data) {//Post一个新窗口
        //url = Data ? 'about:blank' : url;
        var tempForm = document.createElement("form");
        tempForm.id = "tempForm1"
        tempForm.method = "post"
        tempForm.action = url
        tempForm.target = name;
        //console.dir(Data)
        Data += '&_Random=' + parseInt(Math.random() * 1000000000000)
        var kv = Data.split('&')
        for (var i in kv) {
            var _kv = kv[i].split('=')
            var hideInput = document.createElement("input");
            hideInput.type = "hidden";
            hideInput.name = decodeURIComponent(_kv[0])
            if (_kv[1]) {
                hideInput.value = decodeURIComponent(_kv[1].replace(/\+/g, ' '))
            } else {
                hideInput.value = decodeURIComponent(_kv[1])
            }
            tempForm.appendChild(hideInput);
        }
        document.body.appendChild(tempForm);
        tempForm.submit();
        // document.body.removeChild(tempForm);
    }
}


/*全选*/
$(document).on('click', '[checkbox-area]', function () {
    var This = $(this),
        _checked = This.is(':checked')
    var areaId = This.attr('checkbox-area')
    var checkbox_cont = $('.' + areaId + ':visible')
    checkbox_cont = checkbox_cont.length > 0 ? checkbox_cont : $('#' + areaId)
    var checkboxs = checkbox_cont.find(':checkbox:visible')

    checkboxs.each(function (i, ele) {
        var checkboxEle = $(ele)

        checkboxEle.prop('checked', _checked);

    })
}).on('click', '.openwindow', function () {
    var This = $(this)
    var url = This.attr('href'),
        data = This.attr('data'),
        name = This.attr('windowname'),
        fWidth = This.attr('fWidth'),
        fHeight = This.attr('fHeight')
    openwindow(url, name, fWidth, fHeight, data)
    return false
})

// 随机验证码确认
function confirmRandom(text) {
    var random = parseInt(Math.random() * 1000)
    text = text ? text : ''
    return prompt(text + '  请输入:' + random) == random
}

function check_input_empty(ele) {
    var ele = ele ? ele : $('body')
    var check_empty_eles = ele.find('.not-empty')
    var is_check_done = true
    if (check_empty_eles.length > 0) {
        for (var i = 0; i < check_empty_eles.length; i++) {

            if (!check_empty_eles[i].value) {
                inputTooltip(check_empty_eles[i], '<b class="red">不能为空值!</b>', 3000)
                check_empty_eles[i].focus();
                is_check_done = false
                break
            }
        }
    }
    return is_check_done
}

function formatDuration(timeNow, timePublish) {

    var ms1 = Date.parse(timeNow);
    var ms2 = Date.parse(timePublish);
    var ms = ms1 - ms2
    const time = {
        d: Math.floor(ms / 86400000),
        h: Math.floor(ms / 3600000) % 24,
        m: Math.floor(ms / 60000) % 60,
        s: Math.floor(ms / 1000) % 60
    };
    return Object.entries(time)
        .filter(val => val[1] !== 0)
        .map(([key, val]) => `${val}${key}${val !== 1 ? '' : ''}`)
        .join(', ');
};

function diaplayTime(timeNow, timePublish) {
    //将字符串转换成时间格式
    var minute = 1000 * 60;
    var hour = minute * 60;
    var day = hour * 24;
    var month = day * 30;

    var diffValue = timeNow - timePublish;
    var diffMonth = diffValue / month;
    var diffWeek = diffValue / (7 * day);
    var diffDay = diffValue / day;
    var diffHour = diffValue / hour;
    var diffMinute = diffValue / minute;
    var difSec = (diffValue / 1000).toFixed(0)
    if (diffValue < 0) {
        alert("错误时间");
    } else if (diffMonth > 3) {
        result = timePublish.getFullYear() + "-";
        result += timePublish.getMonth() + "-";
        result += timePublish.getDate();

    } else if (diffMonth > 1) {
        result = parseInt(diffMonth) + "M ";
    } else if (diffWeek > 1) {
        result = parseInt(diffWeek) + "W ";
    } else if (diffDay > 1) {
        result = parseInt(diffDay) + "D ";
    } else if (diffHour > 1) {
        result = parseInt(diffHour) + "H ";
    } else if (diffMinute > 1) {
        result = parseInt(diffMinute) + "m " + difSec % 60 + 's';
    } else {
        result = difSec + 's ';
    }

    return result;
}


// daterange
var now = new Date();
var endDateStr = now.Format('yyyy-MM-dd');
var startDate = now.DateAdd('d', -6);
var startDateStr = startDate.Format('yyyy-MM-dd');
var dateRanges = {};
dateRanges[LOCALE_JSON.daterangepicker.ranges.clear] = [null, null];
dateRanges[LOCALE_JSON.daterangepicker.ranges.today] = [moment(), moment()];
dateRanges[LOCALE_JSON.daterangepicker.ranges.yesterday] = [moment().subtract(1, 'days'), moment().subtract(1, 'days')];
dateRanges[LOCALE_JSON.daterangepicker.ranges.beforeYesterday] = [moment().subtract(2, 'days'), moment().subtract(2, 'days')];
dateRanges[LOCALE_JSON.daterangepicker.ranges.last7Days] = [moment().subtract(6, 'days'), moment()];
dateRanges[LOCALE_JSON.daterangepicker.ranges.last30Days] = [moment().subtract(29, 'days'), moment()];
dateRanges[LOCALE_JSON.daterangepicker.ranges.thisMonth] = [moment().startOf('month'), moment().endOf('month')];
dateRanges[LOCALE_JSON.daterangepicker.ranges.lastMonth] = [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')];
dateRanges[LOCALE_JSON.daterangepicker.ranges.last3Months] = [moment().subtract(2, 'month').startOf('month'), moment().subtract(0, 'month').endOf('month')];
dateRanges[LOCALE_JSON.daterangepicker.ranges.lastYear] = [moment().subtract(11, 'month').startOf('month'), moment().subtract(0, 'month').endOf('month')];
dateRanges[LOCALE_JSON.daterangepicker.ranges.thisYear] = [moment().subtract(0, 'year').startOf('year'), moment().subtract(0, 'year').endOf('year')];

// https://www.daterangepicker.cn/#optionss
$(document).on('focus', '.datetime', function () {
    $(this).daterangepicker({
        "minYear": 1970,
        "linkedCalendars": false,
        //"maxDate": moment(),
        "singleDatePicker": true,
        "showDropdowns": true,
        "showWeekNumbers": true,
        "showISOWeekNumbers": true,
        "timePicker": true,
        "timePicker24Hour": true,
        "timePickerSeconds": true,
        "autoUpdateInput": true,
        "ranges": dateRanges,
        "locale": Object.assign(LOCALE_JSON.daterangepicker.locale, {format: 'YYYY-MM-DD HH:mm:ss'})
    }).on("hide.daterangepicker", function (ev, picker) {
        if (!picker.startDate._isValid) {
            $(this).val('')
        }
        this.dispatchEvent(new Event('input'))
    }).on('cancel.daterangepicker', function (ev, picker) {

    })

}).on('focus', '.dateday', function () {
    $(this).daterangepicker({
        "minYear": 1970,
        "linkedCalendars": false,
        //"maxDate": moment(),
        "singleDatePicker": true,
        "showDropdowns": true,
        "showWeekNumbers": true,
        "showISOWeekNumbers": true,
        "autoUpdateInput": true,
        "ranges": dateRanges,
        "locale": Object.assign(LOCALE_JSON.daterangepicker.locale, {format: 'YYYY-MM-DD'})
    }).on("hide.daterangepicker", function (ev, picker) {
        if (!picker.startDate._isValid) {
            $(this).val('')
        }
        this.dispatchEvent(new Event('input'))
    });
}).on('focus', '.time', function () {
    $(this).daterangepicker({
        "minYear": 1970,
        "linkedCalendars": false,
        //"maxDate": moment(),
        "singleDatePicker": true,
        "showDropdowns": true,
        "showWeekNumbers": true,
        "showISOWeekNumbers": true,
        "timePicker": true,
        "timePicker24Hour": true,
        "timePickerSeconds": true,
        "autoUpdateInput": true,
        "ranges": dateRanges,
        "locale": Object.assign(LOCALE_JSON.daterangepicker.locale, {format: 'YYYY-MM-DD HH:mm:ss'})
    }).on("hide.daterangepicker", function (ev, picker) {
        if (!picker.startDate._isValid) {
            $(this).val('')
        }
        this.dispatchEvent(new Event('input'))
    });
}).on('focus', '.daterange', function () {
    $(this).daterangepicker({
        "minYear": 1970,
        "startDate": startDateStr,
        "endDate": endDateStr,
        "linkedCalendars": false,
        // "maxDate": moment(),
        "locale": Object.assign(LOCALE_JSON.daterangepicker.locale, {format: 'YYYY-MM-DD HH:mm:ss'}),
        "ranges": dateRanges,
    }).on("hide.daterangepicker", function (ev, picker) {
        if (!picker.startDate._isValid) {
            $(this).val('')
        }
        //触发DOM对象上的原生input事件
        this.dispatchEvent(new Event('input'))
    });

})
// daterange  end --


// Wdate
$(document).on('focus', '.Wdate', function () {
    WdatePicker({
        dateFmt: 'yyyy-MM-dd HH:mm:ss'
    })
}).on('focus', '.Wdate1', function () {
    WdatePicker({
        dateFmt: 'yyyy-MM-dd'
    })
}).on('focus', '.Wdate2', function () {
    WdatePicker({
        dateFmt: 'HH:mm:ss'
    })
}).on('focus', '.Wdate3', function () {
    WdatePicker({
        dateFmt: 'HH:mm'
    })
}).on('focus', '.Wdate4', function () {
    WdatePicker({
        dateFmt: 'yyyy-MM-dd HH:mm:00'
    })
}).on('focus', '.WdateY', function () {
    WdatePicker({
        dateFmt: 'yyyy-01-01'
    })
}).on('focus', '.WdateM', function () {
    WdatePicker({
        dateFmt: 'yyyy-MM-01'
    })
}).on('focus', '.WdateD', function () {
    WdatePicker({
        dateFmt: 'yyyy-MM-dd'
    })
}).on('focus', '.WdateH', function () {
    WdatePicker({
        dateFmt: 'HH:mm'
    })
}).on('focus', '.WdateW', function () {
    WdatePicker({
        dateFmt: 'yyyy-MM-dd',
        disabledDays: [2, 3, 4, 5, 6, 0]
    })
})
// Wdate end

$(document).on('click', '.ask', function (e) {
    return confirm("确认进行此操作吗 ?")

}).on('click', '.del,.remove,.delete', function () {
    if (confirmRandom('确认删除吗?')) {
        ajax_delete(this)
    }
    return false

}).on('click', '.nav-list a,#home-page,.add_tab', function (e) {
    var tab_concent = parent.window.tab_concent ? parent.window.tab_concent : window.tab_concent
    console.dir(tab_concent)
    stopEevent(e)
    var history_menu = parent.window.history_menu ? parent.window.history_menu : history_menu
    var is_tab = tab_concent.add_tab(this)

    if (history_menu && !$(this).is('#home-page') && is_tab) {
        history_menu.add_history_menu(this)
    }

    return !is_tab

}).on('click', '[data-toggle="popover"]', function (e) {
    if ($(this).attr('data-original-title') == undefined) {
        $(this).popover()
    }
})


function ajaxError(jqXHR, statusText, errorMsg) {
    console.dir(jqXHR)
    console.dir(statusText)
    console.dir(errorMsg)
    try {
        var rsp = JSON.parse(jqXHR.responseText)
        alertError(rsp.msg)
    } catch (e) {
        alertError(jqXHR.statusText)
    }
}

function clearHelpText() {
    $('.help_text').html('')
}

// 根据返回 data 生成 输入框帮助消息
function addHelpText(data, $form) {
    for (k in data) {
        var $input = $form ? $form.find('[name="' + k + '"]') : $('[name="' + k + '"]')

        var $helpTextEle = $('#help_text_' + k)


        if ($helpTextEle.length == 0 && $input.length > 0) {
            $helpTextEle = $('<div id="help_text_' + k + '" class="middle text-danger help_text"></div>')
            $input.after($helpTextEle)
            //$input.focus()
        }
        if ($helpTextEle.length == 0) {

            alertError('error input :' + k + ' : ' + data[k])
        } else {
            $helpTextEle.html(data[k].join(','))
        }
    }


}

// 刷新父窗口表格
function refreshParentTable() {
    parent.refreshTable ? parent.refreshTable() : null
}


function inputTooltip(ele, text, time) {
    var This = $(ele)
    var offset = This.position()
    var span = This.next('.input-tooltip')

    if (span.length == 0) {
        span = $('<span>', {
            "style": "line-height:2em;border-radius: 4px;box-shadow: 2px 2px 3px #969696;cursor: pointer;background-color: white; padding: 0 5px 0 5px;z-index: 999999999;border: 1px solid #AAAAAA;position:absolute;font-weight: bold;",
            "html": "",
            "class": "input-tooltip",
            "click": function () {
                $(this).hide()
            }
        })
        This.after(span)
    }
    var h = 30
    span.css({"left": offset.left, "top": offset.top - h})
    //span.css({"left":offset.left,"top":offset.top-This.innerHeight()-1,"height":This.innerHeight()})
    span.html(text)
    if (text) {
        span.show()
        if (time) {
            span.fadeOut(time)
        }
    } else {
        span.hide()
    }
    return span
}

// 生成提示
function makeToolip(ele, tooltipText, time) {

    var tooltipEle = inputTooltip(ele, tooltipText, time)
    if (tooltipText) {
        tooltipEle.css({'color': 'red'})
    } else {
        tooltipEle.hide()
    }
}

// json 输入框提示
function checkJson(ele) {
    var This = $(ele)
    var tooltipText = ''
    try {
        var j_data = $.parseJSON(This.val())
        tooltipText = typeof j_data == 'object' ? '' : '错误的json格式'
    } catch (e) {
        tooltipText = '错误的json格式'
    }
    makeToolip(ele, tooltipText)
}

$(document).on('keyup', '.check_json,.check-json,.textarea-json', function () {
    $(this).attr('placeholder', '只能JSON格式')
    checkJson(this)

})


//搜索某容器内的checkbox
function searchCheckbox(text, container, callback) {
    var container = typeof container == "string" ? $('#' + container) : container
    container.find("input[type='checkbox']").each(function () {
        var This_checkbox = $(this)
        var This = This_checkbox.parent('label')
        var _html = This.html()
        var checked = This_checkbox.is(':checked')
        if (_html) {
            _html = _html.substr(_html.indexOf('>') + 1)
            if (text.length == 0 || _html.indexOf(text) >= 0 || text.search(',' + _html + ',') >= 0) {
                This.show()
            } else {
                if (!checked) {
                    This.hide()
                }
            }

        }
        if (callback) {
            callback(This_checkbox)
        }
    })
}

function searchTableCheckbox(text, tableId) {
    $('#' + tableId + ' tr').each(function (i, tr) {
        var $tr = $(tr)
        var innerStr = $tr.text()
        if (text.length == 0 || innerStr.indexOf(text) >= 0) {
            $tr.show()
            parant = $tr.find("th label").html()
            // 当左侧内容匹配搜索关键词时，右侧全部展示
            if (parant) {
                parant = parant.substr(parant.indexOf('>') + 1)
                if (text.length == 0 || parant.indexOf(text) >= 0 || text.search(',' + parant + ',') >= 0) {
                    searchCheckbox("", $tr.find('td:last'))
                } else {
                    searchCheckbox(text, $tr.find('td:last'))

                }
            } else {
                searchCheckbox(text, $tr.find('td:last'))
            }

        } else {
            $tr.hide()
        }
    })

}

// 关闭编辑页面保存按钮
function disabledEditBtn() {
    $(function () {
        $('.edit-save-bar').find('input,button,a').attr("disabled", true);
    })

}

// 开启编辑保存按钮
function enabledEditBtn() {
    $('.edit-save-bar').find('input,button,a').removeAttr("disabled");
}

// 设置主题
function setTheme(theme_name) {
    var theme_url = '/static/assets/bootswatch-3/' + theme_name + '/bootstrap.css'
    if (theme_name != 'default') {
        $('#bootswatch-css').attr('href', theme_url)
    } else {
        $('#bootswatch-css').attr('href', '')

    }
    window.localStorage.setItem("theme_name", theme_name);

}

// 加载主题
function loadTheme(theme_name) {
    theme_name = theme_name || window.localStorage.getItem('theme_name')
    if (theme_name) {
        setTheme(theme_name)
    }
}


var search_dbl_cache = {};

//搜索下拉框
function search_dbl_list(dbl_class_name, input_box_class_name) {
    var target = $("." + dbl_class_name);
    if (search_dbl_cache[dbl_class_name + '_is_change']) {
        if (search_dbl_cache[dbl_class_name + '_is_change'])
            return;
    }
    var input_value = $("." + input_box_class_name).val();

    var list = [];
    if (input_value == '') {
        if (search_dbl_cache[dbl_class_name]) {
            list = search_dbl_cache[dbl_class_name];
            target.html('');
        }
    } else {
        var add_to_cache = false;
        target.find('option').each(function () {
            var item = $(this);
            if (!search_dbl_cache[dbl_class_name]) {
                search_dbl_cache[dbl_class_name] = [];
                add_to_cache = true;
            }
            if (add_to_cache) {
                search_dbl_cache[dbl_class_name].push(item);
            }

            if (-1 != item.text().indexOf(input_value)) {
                list.push(item);
            }
        });

        if (list.length == 0 && search_dbl_cache[dbl_class_name]) {
            list = search_dbl_cache[dbl_class_name];
        }
        target.html('');
    }

    for (var i = 0; i < list.length; i++) {
        var item = list[i]
        target.append(item);
        search_dbl_cache[dbl_class_name + '_is_change'] = true;
    }
    search_dbl_cache[dbl_class_name + '_is_change'] = false;
}


$.extend(true, $.fn.bootstrapTable.defaults, {
    locale: BootstrapTableLocale,
    //toolbar: '#toolbar',
    method: "GET", //请求方式（*）
    dataType: "json",
    cache: true,  //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
    pagination: true, //是否显示分页（*）
    sortable: true,  //是否启用排序
    sortOrder: "desc", //排序方式
    resizable: true,
    queryParams: function (params) {
        var paramsArray = $('#filter-form').serializeArray()
        paramsArray.push({name: 'page_size', value: params.pageSize || 10000})
        paramsArray.push({name: 'page', value: params.pageNumber || 1})
        paramsArray.push({name: 'keywords', value: params.searchText})
        var orderPrefix = params.sortOrder == 'asc' ? '' : '-'
        paramsArray.push({name: 'ordering', value: orderPrefix + (params.sortName || '')})
        return paramsArray;

    },//传递参数（*）
    showExport: true,
    totalField: 'count',
    dataField: 'results',
    showJumpTo: "true",
    responseHandler: function (res) {
        if (res.code !== 0) {
            art.dialog.alert(res.msg)
        }
        console.dir(res.data)
        return res.data
    },
    onLoadError: function (status, jqXHR) {
        ajaxError(jqXHR, status)

    },
    sidePagination: "client", //分页方式：client 客户端分页，server 服务端分页（*）
    queryParamsType: "",      //https://examples.bootstrap-table.com/index.html?bootstrap3#options/query-params-type.html
    pageNumber: 1, //初始化加载第一页，默认第一页
    pageSize: 200, //每页的记录行数（*）
    pageList: [200, 400, 600, 2400], //可供选择的每页的行数（*）
    search: true, //是否显示表格搜索，客户端搜索，sidePagination: "server"进服务端
    showSearchClearButton: true,
    strictSearch: false, //严格查询
    showFullscreen: false,
    showColumnsToggleAll: true,
    showColumns: true, //是否显示所有的列
    showRefresh: true, //是否显示刷新按钮
    minimumCountColumns: 2, //最少允许的列数
    clickToSelect: false, //是否启用点击选中行
    multipleSelectRow: false,
    showToggle: false, //是否显示详细视图和列表视图的切换按钮
    cardView: false,   //是否显示详细视图
    detailView: false,//显示详情
    formatLoadingMessage: function () {
        return "";
    }

});


function render_vue_tpl(template_el_id, data, methods) {
    // https://cn.vuejs.org/v2/api/#el
    var methods = methods || {}
    return new Vue({
        delimiters: ['((', '))'],
        template: template_el_id,
        data: data,
        methods: methods

    }).$mount().$el.outerHTML
}

var _hintTimer = null
var IgnoreCodemirrorKeyEvents = ['Backspace', 'Enter', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowUp']

function codemirrorShowHint(editor, event) {
    console.dir(event)
    var ascii_code = event.key.toLowerCase().charCodeAt()
    if (event.key.length == 1 && (ascii_code >= 97 && ascii_code <= 122) && _hintTimer == null) {
        //if (IgnoreCodemirrorKeyEvents.indexOf(event.code) < 0 && _hintTimer == null) {
        _hintTimer = setTimeout(function () {
            editor.showHint({
                completeSingle: false
            })
            _hintTimer = null
        }, 500)

    }
}

// 加载完成事件
$(function () {

    initSelect2()
    initSelectTree()
    initTagsinput()
    loadTheme()

})