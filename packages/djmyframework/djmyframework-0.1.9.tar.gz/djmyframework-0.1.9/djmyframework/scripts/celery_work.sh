#!/bin/sh

celery -A config.celery_app worker -l info -P gevent -c 1000 -E -n `hostname` $*
