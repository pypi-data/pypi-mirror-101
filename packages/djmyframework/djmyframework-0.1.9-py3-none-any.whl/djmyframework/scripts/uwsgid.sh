#!/usr/bin/env sh
# chkconfig: - 85 15
# description: uwsgi 启动脚本
# 使用 init.d需要修改MY_PATH
#

PWD=`pwd`
MY_PATH=$(cd `dirname $0`; pwd)
cd $MY_PATH
mkdir -pv tmp/
export PYTHONUNBUFFERED=TRUE
DATE=`date +%F_%T`

ARGV=$2
APP=""
LOG_FILE="$MY_PATH/logs/uwsgi.log"
CONFIG_FILE="$MY_PATH/config/uwsgi.ini"
PID_FILE="$MY_PATH/tmp/uwsgi.pid"

#基本启动命令不使用daemon模式
BASE_CMD="uwsgi --ini $CONFIG_FILE"

#直接执行脚本, 进入daemon模式
START_CMD="$BASE_CMD -d $LOG_FILE"

#配合-s在supervisord监控启动
[ "$ARGV" == "-s" ] && START_CMD=$BASE_CMD

function kill_server() {
	[ -f $PID_FILE ] && kill -QUIT `cat $PID_FILE` || (pkill -9 -f "$BASE_CMD" )
	sleep 1
	[ "$ARGV" == "-f" ]  && pgrep -f "$BASE_CMD" && (pkill -9 -f "$BASE_CMD" )
	pgrep -f "$BASE_CMD"  || echo "[$BASE_CMD] kill ok!" && rm -f $PID_FILE && return 0
	return 1
}

function start_server() {
	pgrep -f "$BASE_CMD" > /dev/null ||  $START_CMD
	sleep 1  
	pgrep -f "$BASE_CMD" && echo "[$BASE_CMD] start ok!" && return 0
	echo "start error,see $LOG_FILE" && tail  $LOG_FILE
    return 1
}

function reload_server() {
    [ -f $PID_FILE ] && kill -HUP `cat $PID_FILE` && echo "[$BASE_CMD] reload ok!" && tail  $LOG_FILE
    return 0
}


function set_supervisord_config() {

SUPERVISORD_CONFIG_FILE="/etc/supervisord.conf.d/${MY_PATH//\//_}.conf"

cat > $SUPERVISORD_CONFIG_FILE << EOF
[program:${MY_PATH##*/}]
process_name= %(program_name)s
command=$BASE_CMD
directory=$MY_PATH
autorestart=true
redirect_stderr=true
stdout_logfile=$LOG_FILE
stdout_logfile_maxbytes=0
stdout_logfile_backups=0
stdout_capture_maxbytes=0
stdout_events_enabled=false
loglevel = warn
stopsignal=QUIT
killasgroup=true
environment=PYTHONUNBUFFERED="TRUE"
EOF
return 0
}


case $1 in  
    start)
        [ "$ARGV" == "-s" ] && set_supervisord_config
        start_server
        ;;  
    stop)  
        kill_server
        ;;  
    restart)  
        kill_server
        sleep 2
        start_server
        ;;
    reload)
        reload_server
        ;;
    status)
        ps aux | grep  "$BASE_CMD" | grep -v 'grep'
        ;;
    log)  
        tail -f $LOG_FILE
        ;;  
    *)
cat <<EOF
CMD  : [$BASE_CMD]
Usage: $0 start [-s (with supervisord)] | stop [-f force] | restart [-f force]| log | reload | status
EOF
        ;;  
esac  
exit $?