#!/bin/sh

export PYTHONPATH=$(dirname $0):$PYTHONPATH

exec python3 -m bobbit $@
