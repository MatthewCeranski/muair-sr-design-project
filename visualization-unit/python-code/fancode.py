import time
import math
import sqlite3
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import sqlite3
from datetime import datetime
import sqlite3

conn = sqlite3.connect("MUAIRtestdatabase") #connect to database if it exists
conn.row_factory = lambda cursor, row: row[0]
cursor = conn.cursor() #define cursor function

Aqi10 = cursor.execute("SELECT aqi10 FROM aqi10 ORDER BY rowid DESC LIMIT 1").fetchall()
Aqi2p5 = cursor.execute("SELECT aqi25 FROM aqi25 ORDER BY rowid DESC LIMIT 1").fetchall()
#Aqi10=60
#Aqi2p5=1

if Aqi10 > Aqi2p5:
    aqivalue=Aqi10
elif Aqi2p5 > Aqi10:
    aqivalue=Aqi2p5
else:
    aqivalue=Aqi10

print(aqivalue)

RELAIS_1_GPIO=17
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
RELAIS_2_GPIO=17,27
GPIO.setup(RELAIS_2_GPIO, GPIO.OUT)
RELAIS_3_GPIO=17,27,22
GPIO.setup(RELAIS_3_GPIO, GPIO.OUT)
GPIO.output(RELAIS_3_GPIO, GPIO.LOW)
time.sleep(3)

while True:
    if 50 < aqivalue <= 150:
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # Turn on the fan
    elif 150 < aqivalue <= 300:
        GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # Turn on the fan
    elif 300 < aqivalue < 10000:
        GPIO.output(RELAIS_3_GPIO, GPIO.HIGH) # Turn on the fan
    else:
        GPIO.output(RELAIS_3_GPIO, GPIO.LOW)