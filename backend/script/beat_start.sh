#!/bin/sh

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery --app app beat -l INFO