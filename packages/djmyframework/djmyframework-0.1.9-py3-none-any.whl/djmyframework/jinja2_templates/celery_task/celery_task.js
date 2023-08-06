// 查询 celery 返回信息
function CelertTasKResult(field_name, $bootstrap_table, query_interval, loading_text, allow_err_num) {
    var query_interval = query_interval || 3000
    var field_name = field_name || 'status'
    var loading_text = loading_text || '查询中...'


    var allow_err_num = allow_err_num || 30
    var task_num = 0
    var err_num = 0
    var _this = this

    this.task_id_map = {}
    this.query_task_timer = null
    var _this = this

    this.done_status = eval("{{data.done_status | safe}}")


    function check_task_finish(task) {
        return _this.done_status.indexOf(task.status) >= 0
    }

    // 更新任务执行状态
    this._updateTableStatus = function (task_ids, task) {

        if ($bootstrap_table == undefined) {
            return
        }
        for (var i in task_ids) {

            var task_id = task_ids[i]
            var row_id = _this.task_id_map[task_id]
            var status_text = ''
            if (!row_id) {
                return
            }
            if (task.task_name) {
                status_text = task.task_name.split('.').pop() //+ ':' + task.status
                status_text = task.status == 'FAILURE' ? task.traceback : status_text
            }
            var sourceFieldLookup = '_source_' + field_name
            var rowData = $bootstrap_table.bootstrapTable('getRowByUniqueId', row_id)

            if (check_task_finish(task)) {
                $bootstrap_table.bootstrapTable('uncheckBy', {field: 'id', values: [row_id]})
                status_text += '<span class="glyphicon glyphicon-ok-circle"></span>'
                rowData.executing = false
            } else {
                status_text += '<img src="/static/images/loading.gif">'
                rowData.executing = true
            }

            if (rowData[sourceFieldLookup] == undefined) {
                rowData[sourceFieldLookup] = rowData[field_name] || ''
            }
            var sourceText = rowData[sourceFieldLookup]
            rowData[field_name] = sourceText + status_text
            $bootstrap_table.bootstrapTable('updateByUniqueId', {
                id: row_id,
                row: rowData
            })
        }

    }


    this.queryTaskResult = function (id_task_id_map, callback) {
        clearInterval(_this.query_task_timer)
        var task_queue = Object.values(id_task_id_map)
        task_num = err_num = 0
        for (id in id_task_id_map) {
            _this.task_id_map[id_task_id_map[id]] = id
        }
        _this._updateTableStatus(task_queue, {status: ''})
        _this.query_task_timer = setInterval(function () {

            if (task_queue.length <= 0) {
                clearInterval(_this.query_task_timer)
                return
            }

            $.get("{{ url('celery_task.query') }}", {task_id: task_queue}, function (rsp) {
                    if (rsp.code == 0) {
                        var task_list = rsp.data
                        if (task_list.length == 0) {
                            err_num += 1
                            // updateStatus(task_queue, {status: err_num + '次查询.'})
                        }

                        if (err_num >= allow_err_num) {

                            clearInterval(_this.query_task_timer)
                            _this._updateTableStatus(task_queue, {status: err_num + '次查询错误.'})
                        }
                        for (var i in task_list) {
                            var task = task_list[i]
                            _this._updateTableStatus([task.task_id], task)
                            if (check_task_finish(task)) {
                                task_queue.splice(task_queue.indexOf(task.task_id), 1)
                            }
                            var row_id = _this.task_id_map[task.task_id]
                            var is_all_done = task_queue.length == 0
                            callback ? callback(row_id, task, is_all_done, rsp) : null
                        }

                    } else {
                        alert('query celery result error')
                        clearInterval(_this.query_task_timer)
                    }

                }, 'json'
            ).fail(function () {
                console.dir('Fail query task status')
                console.dir('task_queue')
            })
        }, query_interval)

        return _this
    }

    // 撤销任务
    this.revokeExecuteTask = function (progress_task_result, task_ids, callback) {
        if (!task_ids) {
            task_ids = []
            task_ids = $.map(progress_task_result, function (row) {
                return task_ids = task_ids.concat(row.task_result_id)
            })
        }

        $.post("{{ url('celery_task.revoke_task') }}", {task_id: task_ids}, (rsp) => {
                callback(rsp)
            }
        )
    }

    // 查询正在执行的任务
    this.queryProgressTask = function (a_ids, a_type_names, callback) {
        $.getJSON("{{ url('celery_task.query_progress') }}", {
                a_id: a_ids,
                a_type_name: a_type_names
            }, (rsp) => {
                callback(rsp)

            }
        )
    }

}
