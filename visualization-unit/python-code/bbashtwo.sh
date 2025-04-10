#!/bin/bash

if pgrep -f "mqttstoretrial.py"; then
	echo "running"
	exit
else
	echo "not running"
	cd /home/muair/RunMUAIR_vis
	python mqttstoretrial.py
	exit

fi