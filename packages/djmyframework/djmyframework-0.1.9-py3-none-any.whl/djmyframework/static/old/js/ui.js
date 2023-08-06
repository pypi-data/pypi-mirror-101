$('.submit').click(function () {
    $('form:first').submit()
})

//http://datatables.net/plug-ins/pagination#bootstrap
$.extend(true, $.fn.dataTable.defaults, {
    "dom": "<'row'<'col-sm-3'f><'col-sm-3'><'col-sm-6 datatable_toolbar'>>rt<'row'<'col-sm-2'i><'col-sm-2'l><'col-sm-8'p>>",
    "renderer": "bootstrap",
});


//根据元素id获取模版
window.get_tmpl = function (id) {
    return document.getElementById(id).innerHTML
}
//返回渲染的模版
window.get_views = function (tmpl_id, obj) {
    var data = {"w": window}
    data['data'] = obj

    return doT2.template(window.get_tmpl(tmpl_id))(data)
}

function alertError(msg) {
    msg = msg.replace(/\n/, '<br>')
    return art.dialog({
        title: 'Alert',
        content: '<div class="pre-scrollable alert alert-danger">' + msg + '</div>',
        id: msg
    })
}

// 用户界面相关

/* 分页 */
function goPage(pageNum) {
    var pageUrl = document.location.href;
    pageUrl = pageUrl.replace(/page_num=\d+/, '')

    var _form = $("form:first")
    if (_form.attr('method') && _form.attr('method').toLowerCase() == 'post') {
        _form.append($('<input type="hidden" name="page_num" value="' + pageNum + '">'))
        _form.submit();
    } else {
        if (pageUrl.indexOf("?") == -1) {
            pageUrl += "?"
        }
        if (pageUrl.substr(pageUrl.length - 1, 1) == "&") {
            pageUrl = pageUrl.substr(0, pageUrl.length - 1);
        }
        var url = pageUrl + "&page_num=" + pageNum;
        document.location.href = url;
    }

}

function change_page(ele) {
    var pageNum = $(ele).val()
    if (!isNaN(pageNum) && pageNum) {
        goPage(parseInt(pageNum))
    }
}

/*分页
@pageNum 当前页数
@pageSize 页条目数
@totalRecord 总条目数
*/
function pager_post(pageNum, pageSize, totalRecord) {
    var totalPage = parseInt(totalRecord / pageSize);
    if (totalRecord % pageSize != 0)
        totalPage++;

    var pageUrl = document.location.href;
    pageUrl = pageUrl.replace(/page_num=\d+/, '')
    if (pageUrl.indexOf("?") == -1)
        pageUrl += "?"

    if (pageUrl.substr(pageUrl.length - 1, 1) != "&" && pageUrl.substr(pageUrl.length - 1, 1) != "?")
        pageUrl += "&";

    var pagerHtml = "每页 <font color='red'>" + pageSize + "</font>条 共 <font color='red'>" + totalRecord + "</font>条记录&nbsp&nbsp";
    if (pageNum > 1) {
        pagerHtml += "<a href='javascript:goPage(" + 1 + ");'>第一页</a>";
        pagerHtml += "<a href='javascript:goPage(" + (pageNum - 1) + ");'>上一页</a>";
    }
    var sPageNum = pageNum - 4;
    if (sPageNum < 1)
        sPageNum = 1;
    var ePageNum = sPageNum + 10;
    if (ePageNum > totalPage)
        ePageNum = totalPage;

    for (var i = sPageNum; i <= ePageNum; i++) {
        if (i == pageNum)
            pagerHtml += '<span>' + i + '</span>';
        else
            pagerHtml += "<a href='javascript:goPage(" + i + ");'>" + i + "</a>";
    }

    if (pageNum < totalPage) {
        pagerHtml += "<a href='javascript:goPage(" + (pageNum + 1) + ");'>下一页</a>";
        pagerHtml += "<a href='javascript:goPage(" + totalPage + ");'>最后一页</a>";
    }
    if (pageNum && totalPage && pageNum > totalPage) {
        goPage(parseInt(totalPage))
    }
    pagerHtml += '&nbsp共&nbsp' + totalPage + '&nbsp页&nbsp&nbsp'
    pagerHtml += '<input type="text" style="width:30px; margin:0px; padding:0px;" onblur="change_page(this)" value="" > ';

    $("#pager").html(pagerHtml);
}

/* 兼容 GET */
function pager(pageNum, pageSize, totalRecord) {
    pager_post(pageNum, pageSize, totalRecord)
}

// page end

var search_dbl_cache = {};


//datatable 扩展
(function ($) {
    $.fn.dataTableExt.oApi.fnGetColumnData = function (oSettings, iColumn, bUnique, bFiltered, bIgnoreEmpty) {
        // check that we have a column id
        if (typeof iColumn == "undefined") return new Array();
        // by default we only want unique data
        if (typeof bUnique == "undefined") bUnique = true;
        // by default we do want to only look at filtered data
        if (typeof bFiltered == "undefined") bFiltered = true;
        // by default we do not want to include empty values
        if (typeof bIgnoreEmpty == "undefined") bIgnoreEmpty = true;
        // list of rows which we're going to loop through
        var aiRows;
        // use only filtered rows
        if (bFiltered == true) aiRows = oSettings.aiDisplay;
        // use all rows
        else aiRows = oSettings.aiDisplayMaster; // all row numbers
        // set up data array
        var asResultData = new Array();
        for (var i = 0, c = aiRows.length; i < c; i++) {
            iRow = aiRows[i];
            var aData = this.fnGetData(iRow);
            var sValue = aData[iColumn];
            // ignore empty values?
            if (bIgnoreEmpty == true && sValue.length == 0) continue;
            // ignore unique values?
            else if (bUnique == true && jQuery.inArray(sValue, asResultData) > -1) continue;
            // else push the value onto the result data array
            else asResultData.push(sValue);
        }
        return asResultData;
    }
    //增加select框
    $.fn.dataTableExt.oApi.fnAddSelect = function (oSettings, aColumnIndexs) {
        var oDatatable = this
        aColumnIndexs = aColumnIndexs ? aColumnIndexs : []

        function fnCreateSelect(aData) {
            var r = '<select><option value=""></option>', i, iLen = aData.length;
            for (var i = 0; i < iLen; i++) {
                var _val = aData[i].replace(/<[^>]+>|\r|\n|\t|\s*/g, "")
                r += '<option value="' + _val + '">' + _val + '</option>';
            }
            return r + '</select>';
        }

        var tds_html = ''
        this.find('thead th').each(function (i, ele) {
            tds_html += '<td class="datatable-select-td"></td>'
        })
        this.find('thead').after('<thead><tr>' + tds_html + '</tr></thead>')
        this.find('.datatable-select-td').each(function (i) {
            if ($.inArray(i, aColumnIndexs) >= 0 || aColumnIndexs.length == 0) {
                this.innerHTML += fnCreateSelect(oDatatable.fnGetColumnData(i));
                $('select', this).change(function () {
                    oDatatable.fnFilter($(this).val(), i);
                });
            }
        });

    }
}(jQuery));

// 设置input值
function inputText(inputName, inputValue) {
    $("input[name='" + inputName + "']").val(inputValue);
}


function enfoldment(id) {
    $('#' + id).toggleClass('enfoldment');
}

// checkbox 颜色
function change_checkbox_background(eles) {
    eles = eles ? eles : $(':checkbox')
    eles.each(function (i, ele) {
        var _e = $(ele)
        if (_e.is(':checked')) {
            _e.parent('label').addClass('checked')
        } else {
            _e.parent('label').removeClass('checked')
        }
    })
}

$(document).on('click', 'label>:checkbox', function () {
    change_checkbox_background($(this))
})


var selectId = 0
$(document).ready(function () {

    //select增加svalue为默认选择
    $("select[svalue]").each(function () {
        target = $(this);
        var value = target.attr('svalue');
        if (value == '') {
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


    // -- datatable --
    $('.datatable').each(function (index, ele) {
        var tableObj = $(ele)
        var opt = {
            "sDom": "<'row'<'col-sm-3'f><'col-sm-3'><'col-sm-6 datatable_toolbar'>>rt<'row'<'col-sm-2'i><'col-sm-2'l><'col-sm-8'p>>",
            //"sScrollY": '200px',//document.documentElement.clientHeight*0.6 + 'px',
            //"bScrollCollapse": true,
            //"sScrollX": "100%",
            //"sScrollXInner": "100%",
            "fixedHeader": true,
            "footer": true,
            "bSortClasses": false,
            "bStateSave": false,
            "bProcessing": true, //是否显示正在处理的提示
            "iDisplayLength": -1,//默认每页显示的记录数
            "bPaginate": false, // 是否使用分页
            "aLengthMenu": [50, 100, 1000],
            "bAutoWidth": false,//列的宽度会根据table的宽度自适应
            //"bSortClasses":true,
            "bLengthChange": true,//分页栏
            "oSearch": {
                "sSearch": "",//默认的框文字
                "bRegex": true,//支持正则搜索
            },
            "bInfo": true,
            "oLanguage": {
                "sSearch": "筛选:",//
                "sZeroRecords": "没有匹配记录",
                "sInfo": '当前 _START_ - _END_ 条 共 _TOTAL_ 条',
                "sInfoFiltered": "(从 _MAX_ 条记录中过滤)",
                "sLengthMenu": "每页显示 _MENU_条",
                "sProcessing": "正在加载数据...",
                "sInfoEmpty": "",
                "oPaginate": {
                    "sFirst": "首页",
                    "sPrevious": "前一页",
                    "sNext": "后一页",
                    "sLast": "尾页"
                }

            },
            "aoColumnDefs": [],
            "aaSorting": [] //默认不排序
        }
        var checkboxIndex = tableObj.find('th>:checkbox').index()//checkbox的列不排序
        if (checkboxIndex >= 0) {
            opt["aoColumnDefs"].push(
                {
                    "bSortable": false,
                    "aTargets": [checkboxIndex]
                }
            )
        }
        opt["bInfo"] = tableObj.attr("data-bInfo") == 'false' ? false : true
        var oDatatable = tableObj.dataTable(opt)
        var toolbarId = tableObj.attr('data-toolbar')
        toolbarId = toolbarId ? toolbarId : 'datatable_toolbar'
        toolbarEle = $('#' + toolbarId)
        toolbarEle.appendTo(oDatatable.parent().find('.datatable_toolbar'))
        // toolbarEle.find('[href]').click(function(){
        // 	//alert(tableObj.find('[name]').serialize())

        // })
        var group_by_index = tableObj.attr('data-group-by-index')//分组
        if (group_by_index) {
            oDatatable.fnAddSelect($.parseJSON(group_by_index))
        }
    });

    //树表格
    $(".treetable").treetable(
        {expandable: true, clickableNodeNames: false}
    ).on('dblclick', 'tbody>tr', function () {
        var This = $(this)
        var tt_id = This.attr("data-tt-id")
        var action = This.find('[title="Expand"]').length > 0 ? "expandNode" : "collapseNode"
        This.closest('.treetable').treetable(action, tt_id)
    })

    // table 选中
    $('.datatable,.treetable').on("mousedown", "tbody>tr", function (e) {
        $(".selected").not(this).removeClass("selected");
        var This = $(this)

        selectId = 0
        This.toggleClass("selected");
        if (This.hasClass('selected')) {
            selectId = This.attr('trid') ? This.attr('trid') : This.find(':checkbox').val()
        }

        // if (!$(e.target).is(':checkbox')) {
        // 	This.find(':checkbox').click();
        // }
    })


    $('.submit').click(function () {
        $('form:first').submit()
    })
    change_checkbox_background()

    /* 选择框 */
    $(".chosen-select").chosen();

    $('.table-menu a').mousemove(function (event) {
        $(this).addClass('active')
        $('.table-menu a').not(this).removeClass('active')
    });


    $('.spinner1').ace_spinner({
        value: 0,
        min: 0,
        max: 200,
        step: 10,
        btn_up_class: 'btn-info',
        btn_down_class: 'btn-info'
    })
        .on('change', function () {
            //alert(this.value)
        });

    // 下拉菜单悬停
    $('.dropdown-menu-not-hide').click(function (e) {
        e.stopPropagation()
    })
})


/*输入框增加下拉选择
	input 控件属性
	@select_key 获取字典列表的key
	@value_forat 自动填值时额外的格式
*/
function SelectInput() {
    var This = this
    var ignore_keys = ['img_path_format',] //特殊用途的key
    var _div = $("#follow_div")

    /*
    初始化和绑定事件
    */
    this.init = function () {
        //初始化,增加一个跟踪控件的div
        if (_div.length == 0) {
            _div = $('<div>', {"id": "follow_div"})
            $(document.body).append(_div)
            //外层点击事件
            $('body').click(function (evt) {
                if ($(evt.target).parents("#follow_div").length == 0 &&
                    !$(evt.target).attr('select-key') && evt.target.id != "follow_div") {
                    $('#follow_div').hide();
                }
            });
        }

        $('[select_key]').each(function (i, ele) {
            var _This = $(ele)
            var _interface_key = _This.attr('select_key')
            _This.removeAttr('select_key')
            _This.attr('select-key', _interface_key)
            // _This.focus(function(event) {
            // 	This.show_div($(this),_This)

            // });
            // _This.keyup(function(event) {
            // 	This.search(_This.val())
            // });
        })


        $(document).on('focus', '[select-key]', function () {
            This.show_div($(this), $(this))

        }).on('keyup', '[select-key]', function () {
            This.search($(this))
        })


        /* 初始化 chosen控件添加选项*/
        function chosenInit(k_v, ele) {
            var textFormat = ele.attr('value_format')
            for (var k in k_v) {
                if ($.inArray(k, ignore_keys) >= 0 || k == '') {
                    continue
                }
                var text = k_v[k]

                if (textFormat) {
                    text = textFormat.replace(/__key__/g, k).replace(/__value__/, k_v[k])
                }
                ele.append("<option value='" + k + "'>" + text + "</option>");

            }
            var default_value = ele.attr('data-default-value')
            ele.attr('chosen-key', ele.attr('chosen_key'))
            ele.removeAttr('chosen_key')
            if (default_value) {
                try {
                    default_value = $.parseJSON(default_value)
                } catch (e) {
                    console.dir(default_value)
                }
                ele.val(default_value)
            }
            ele.chosen({"search_contains": true})
        }

        $('select[chosen_key]').each(function (i, ele) {
            var chosenSelectEle = $(ele)
            var select_key = chosenSelectEle.attr('chosen_key')
            This.get_dict(select_key, chosenSelectEle, chosenInit)
        })

        function tagInit(k_v, ele) {
            ele.attr('tag-key', ele.attr('chosen_key'))
            ele.removeAttr('tag_key')
            //we could just set the data-provide="tag" of the element inside HTML, but IE8 fails!
            var tag_input = ele;
            var values = []
            $.each(k_v, function (k, v) {
                values.push(v)
            })
            console.dir(values)
            if (!(/msie\s*(8|7|6)/.test(navigator.userAgent.toLowerCase()))) {
                tag_input.tag(
                    {
                        placeholder: tag_input.attr('placeholder'),
                        //enable typeahead by specifying the source array
                        source: values,//defined in ace.js >> ace.enable_search_ahead
                    }
                );
            } else {
                //display a textarea for old IE, because it doesn't support this plugin or another one I tried!
                tag_input.after('<textarea id="' + tag_input.attr('id') + '" name="' + tag_input.attr('name') + '" rows="3">' + tag_input.val() + '</textarea>').remove();
                //$('#form-field-tags').autosize({append: "\n"});
            }
        }


        $('input[tag_key]').each(function (i, ele) {
            var tagSelectEle = $(ele)
            var select_key = tagSelectEle.attr('tag_key')
            This.get_dict(select_key, tagSelectEle, tagInit)
        })


    }
    this.search = function ($ele) {
        var value = $ele.val()
        var is_multiple = $ele.attr('data-multiple')

        _div.find('.select-a').each(function (i, _ele) {
            var __ele = $(_ele)
            if (__ele.text().indexOf(value) >= 0 || is_multiple) {
                $(__ele).parent('li').show()
            } else {
                $(__ele).parent('li').hide()
            }
        });


    }
    this.show_div = function (follow_obj, input_obj) {
        //if(_div.is(":hidden")){
        var x = follow_obj.offset();
        _div.css({"left": x.left, "top": x.top + follow_obj.outerHeight() - 1, "min-width": input_obj.innerWidth()})
        var _key = input_obj.attr('select-key')
        _div.html('载入中...')
        This.get_dict(_key, input_obj, This.padding_div)
        _div.show()
        //}
    }

    this.padding_div = function (json, input_obj) {
        var contains = _div

        if (contains.find('a').length == 0) {
            contains.html('')
            var is_multiple = input_obj.attr('data-multiple') == 'true'
            var _ul = $('<ul>', {"class": "select-ul"})
            //if (is_multiple) {
            contains.append($('<input>', {
                "type": "text", "class": "input-small", "placeholder": "搜索", "keyup": function () {
                    This.search($(this))
                }
            }))
            //}
            contains.append(_ul)
            var _img_url_format = ''
            var value_format = input_obj.attr('value_format') ? input_obj.attr('value_format') : '__key__'
            var text_format = input_obj.attr('text_format') ? input_obj.attr('text_format') : '__value__(__key__)'
            if (json.img_path_format) {
                _img_url_format = '/static/img/' + json.img_path_format
            }
            var _key_list = [];
            $.each(json, function (key, val) {
                _key_list.push(key);
            });
            _key_list.sort()
            for (var _i in _key_list) {
                var k = _key_list[_i]
                var _li = $('<li>', {"class": "select-li"})
                if ($.inArray(k, ignore_keys) >= 0 || k == '') {
                    continue
                }

                var _value = json[k]
                var _invalue = value_format.replace(/__key__/g, k)
                var test = text_format.replace(/__key__/g, k).replace(/__value__/g, _value)
                var _a = $('<a>', {
                    "html": test,
                    "href": "javascript:void(0)",
                    "value": k,
                    invalue: _invalue,
                    "title": k,
                    "class": 'select-a'
                })
                _a.click(function (event) { //点击事件

                    var select_value = $(this).attr('invalue')
                    if (is_multiple) {
                        var invalue = input_obj.val()
                        if (invalue.match(/,$/) || !invalue) {
                            invalue += select_value
                        } else {
                            invalue += ',' + select_value
                        }
                        select_value = invalue
                    }

                    input_obj.val(select_value)
                    do_change(select_value, input_obj)
                    contains.hide()
                })
                if (_img_url_format) {
                    _a.mouseenter(function (event) {
                        var This = $(this)
                        var item_img_url = _img_url_format.replace(/__key__/g, This.attr('value'))
                        var _img = $('<img>', {
                            "src": item_img_url,
                            "alt": This.text(),
                            "class": "select-img",
                            "error": function () {
                                this.src = '/static/img/err.png'
                            }
                        })
                        This.after(_img)
                    });
                    _a.mouseout(function () {
                        $(this).next('img').remove()
                    })
                }
                _li.append(_a)
                _ul.append(_li)
            }
        }
        This.search(input_obj)
    }
    //获取字段到a标签 callback(json,input_obj )
    this.get_dict = function (key, input_obj, callback) {
        var k_v = null
        if (key.indexOf('{') >= 0) {
            try {
                k_v = $.parseJSON(key)
            } catch (e) {
                console.dir(e)
            }
        } else {
            var built_data = input_obj.data(key)
            k_v = built_data ? built_data : _div.data(key)
        }

        if (k_v) {
            callback(k_v, input_obj)
        } else {
            var _url = '/log/dict/interface?key=' + key
            $.getJSON(_url, {}, function (json) {
                _div.data(key, json)
                callback(json, input_obj)
            });
        }
    }
}

function do_change() {

}

function make_toolip(ele, tooltipText, time) {

    var tooltipEle = inputTooltip(ele, tooltipText, time)
    if (tooltipText) {
        tooltipEle.css({'color': 'red'})
    } else {
        tooltipEle.hide()
    }
}


$(document).on('blur', '.input-number', function () {
    var tooltipText = ''
    var $this = $(this)
    var value = $this.val()

    if (isNaN(value) || value.length == 0) {
        tooltipText = '输入的不是数字 !'
        //alert(tooltipText)
        $this.val(value.replace(/[^\d-\.]+/g, ''))
        //this.focus();
    }

    value = parseInt(value)
    if (value > 10000) {
        tooltipText = parseInt(value / 10000) + ' 万'
    }
    make_toolip(this, tooltipText, 5000)

}).on('blur', '.letter,.input-letter', function () {
    make_toolip(this, this.value.replace(/[a-zA-Z-_]+/g, '') != '' ? '输入的不是纯字母!' : '')
})


//var select_input = new SelectInput()

$(document).ready(function () {
    //select_input.init()
    change_checkbox_background()
})
