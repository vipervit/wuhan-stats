#!/bin/bash

kill -9 `ps -ef | grep wuhan | awk '{print $2}'`
