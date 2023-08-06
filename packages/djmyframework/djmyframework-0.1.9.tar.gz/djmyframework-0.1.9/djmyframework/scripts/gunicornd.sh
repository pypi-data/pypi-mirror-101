#!/usr/bin/env sh
# chkconfig: - 85 15
# description: gunicorn 启动脚本
# 使用 init.d需要修改MY_PATH
#
# http://docs.gunicorn.org/en/latest/signals.html,supervisorctl signal HUP all

PWD=`pwd`
MY_PATH=$(cd `dirname $0`; pwd)
MY_PATH=$PWD
cd $MY_PATH
PROGRAM="${MY_PATH##*/}"

ARGV=$2

LOG_FILE="$MY_PATH/logs/gunicorn.log"
PID_FILE="$MY_PATH/tmp/gunicorn.pid"
CONFIG_FILE="$MY_PATH/config/gunicorn_config.py"

[ ! -f "$CONFIG_FILE" ] && echo "$CONFIG_FILE not exists" && exit

APP="wsgi"
BIND="0.0.0.0:8080"


#基本启动命令不使用daemon模式
BASE_CMD="gunicorn $APP -c $CONFIG_FILE"

export PYTHONUNBUFFERED=TRUE
START_CMD="$BASE_CMD --error-logfile $LOG_FILE --access-logfile $LOG_FILE --pid $PID_FILE"

#配合-s在supervisord监控启动
[ "$ARGV" == "-s" ] && START_CMD=$BASE_CMD


function kill_server() {
	[ -f $PID_FILE ] && kill -TERM `cat $PID_FILE` || (pkill -9 -f "$BASE_CMD" )
	sleep 1
	[ "$ARGV" == "-f" ] && pgrep -f "$BASE_CMD" && (pkill -9 -f "$BASE_CMD" )
	pgrep -f "$BASE_CMD"  || echo "[$BASE_CMD] kill ok!" && rm -f $PID_FILE && return 0
	return 1
}

function start_server() {
    [ -d tmp ] || mkdir -pv tmp
	pgrep -f "$BASE_CMD" > /dev/null ||  $START_CMD
	sleep 1
	pgrep -f "$BASE_CMD" && echo "[$BASE_CMD] start ok!" && tail  $LOG_FILE && return 0
	echo "start error,see $LOG_FILE" && tail  $LOG_FILE
    return 1
}

function reload_server() {
    [ -f $PID_FILE ] && kill -HUP `cat $PID_FILE` && echo "[$BASE_CMD] reload ok!" && tail  $LOG_FILE
    return 0
}


function set_supervisord_config() {

SUPERVISORD_CONFIG_FILE="/etc/supervisord.conf.d/${MY_PATH//\//_}_$PROGRAM.conf"

cat > $SUPERVISORD_CONFIG_FILE << EOF
[program:$PROGRAM]
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
stopsignal=TERM
killasgroup=true
environment=PYTHONUNBUFFERED="TRUE"
EOF
return 0
}



function set_logrotate() {

LOGROTATE_FILE=${LOG_FILE//\//_}
LOGROTATE_FILE=${LOGROTATE_FILE//./_}
LOGROTATE_FILE="/etc/logrotate.d/$LOGROTATE_FILE"

[ -f "$LOGROTATE_FILE" ] || echo "add LOGROTATE $LOGROTATE_FILE"

cat > $LOGROTATE_FILE <<EOF
"$LOG_FILE" {
    daily
    missingok
    dateext
    dateformat -%Y-%m-%d.%s
    rotate 30
    #compress
    delaycompress
    #notifempty
    create 640 root root
    sharedscripts
    postrotate
        [ -f "$PID_FILE" ] && kill -USR1 \`cat $PID_FILE\` >/dev/null 2>&1
    endscript
}
EOF
return 0
}



case $1 in
    start)
        [ "$ARGV" == "-s" ] && set_supervisord_config
        set_logrotate
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

