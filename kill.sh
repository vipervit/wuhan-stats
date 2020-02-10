#!bin/bash

kill -9 `ps -ef | grep wuhan-stats | awk '{print $2}'` >/dev/null 2>&1
