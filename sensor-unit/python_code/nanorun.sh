#!/bin/bash

if pgrep -f "nano_run.py"; then
	echo "running"
	exit
else
	echo "not running"
	cd /home/muair/RunMUAIR
	python nano_run.py
	exit
fi