/*输入框增加下拉选择
	input 控件属性
	@select_key 获取字典列表的key
	@value_forat 自动填值时额外的格式
*/
function SelectInput2() {
    var This = this
    var ignore_keys = ['img_path_format',] //特殊用途的key
    var _div = $("#follow_div")

    /*
    初始化和绑定事件
    */
    this.init = function () {
        //初始化,增加一个跟踪控件的div
        if (_div.length == 0) {
            _div = $('<div>', {"id": "follow_div","style":'    position: absolute;\n' +
                    '    overflow: auto;\n' +
                    '    border: 1px solid #778899;\n' +
                    '    background: white;\n' +
                    '    max-height: 300px;\n' +
                    '    width: auto;\n' +
                    '    padding: 5px 0px 5px 0px;\n' +
                    '    border-radius: 0px 0px 5px 5px;\n' +
                    '    z-index: 99999999;\n' +
                    '    display: none;'})
            $(document.body).append(_div)
            //外层点击事件
            $('body').click(function (evt) {
                if ($(evt.target).parents("#follow_div").length == 0 &&
                    !$(evt.target).attr('data-select-key') && evt.target.id != "follow_div") {
                    $('#follow_div').hide();
                }
            });
        }


        $(document).on('focus', '[data-select-key],[data-select_key]', function () {

            This.show_div($(this), $(this))


        }).on('keyup', '[data-select-key]', function () {
            This.search($(this))
        })



        /* 初始化 chosen控件添加选项*/
        function chosenInit(k_v, ele) {
            var textFormat = ele.attr('text_format')
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
            ele.select2({
                width: 'auto',
                placeholder: '请选择',
                language: BootstrapTableLocale,
                allowClear: true,
                theme: "bootstrap"
            })
        }

        $('select[chosen_key]').each(function (i, ele) {
            var chosenSelectEle = $(ele)
            var select_key = chosenSelectEle.attr('chosen_key')
            var k_v = chosenSelectEle.attr('data-dict')
            if (k_v) {
                k_v = $.parseJSON(k_v)
                chosenInit(k_v, chosenSelectEle)
            } else {
                This.get_dict(select_key, chosenSelectEle, chosenInit)
            }
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
        var _key = input_obj.attr('data-select-key')
        input_obj.attr('data-has-init-select',true)
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
            var value_format = input_obj.attr('data-value-format') ? input_obj.attr('data-value-format') : '__key__'
            var text_format = input_obj.attr('data-text-format') ? input_obj.attr('data-text-format') : '__value__(__key__)'
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
            var _url = '/log_def/dict_define/interface?key=' + key
            $.getJSON(_url, {}, function (rsp) {
                var data=rsp.data
                _div.data(key, data)
                callback(data, input_obj)
            });
        }
    }

}
var select_input2 = new SelectInput2()

$(document).ready(function() {
	select_input2.init()
})