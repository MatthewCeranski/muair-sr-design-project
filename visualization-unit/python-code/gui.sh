#!/bin/bash

if pgrep -f "gui_run.py"; then
	echo "running"
	exit
else
	echo "not running"
	cd /home/muair/RunMUAIR
	python gui_run.py &
	chromium-browser --start-fullscreen http:127.0.0.1:8050
	exit
fi

