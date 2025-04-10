import sys
import os
import paho.mqtt.client as mqtt
import time
import sqlite3

conn = sqlite3.connect("MUAIRtestdatabase") #connect to database if it exists
conn.row_factory = lambda cursor, row: row[0]
cursor = conn.cursor() #define cursor function

serv='10.162.25.103'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(serv, 1883,60)

client.loop_start()

UTC, = cursor.execute("SELECT time FROM temp ORDER BY rowid DESC LIMIT 1").fetchall()

Aqi10, = cursor.execute("SELECT aqi10 FROM aqi10 ORDER BY rowid DESC LIMIT 1").fetchall()
Aqi2p5, = cursor.execute("SELECT aqi25 FROM aqi25 ORDER BY rowid DESC LIMIT 1").fetchall()

PM1Sens1, = cursor.execute("SELECT sensor1 FROM pm1 ORDER BY rowid DESC LIMIT 1").fetchall()
PM1Sens2, = cursor.execute("SELECT sensor2 FROM pm1 ORDER BY rowid DESC LIMIT 1").fetchall()
PM1Sensavg, = cursor.execute("SELECT avg FROM pm1 ORDER BY rowid DESC LIMIT 1").fetchall()

PM2p5Sens1, = cursor.execute("SELECT sensor1 FROM pm2p5 ORDER BY rowid DESC LIMIT 1").fetchall()
PM2p5Sens2, = cursor.execute("SELECT sensor2 FROM pm2p5 ORDER BY rowid DESC LIMIT 1").fetchall()
PM2p5Sensavg, = cursor.execute("SELECT avg FROM pm2p5 ORDER BY rowid DESC LIMIT 1").fetchall()

PM4Sens1, = cursor.execute("SELECT sensor1 FROM pm4 ORDER BY rowid DESC LIMIT 1").fetchall()
PM4Sens2, = cursor.execute("SELECT sensor2 FROM pm4 ORDER BY rowid DESC LIMIT 1").fetchall()
PM4Sensavg, = cursor.execute("SELECT avg FROM pm4 ORDER BY rowid DESC LIMIT 1").fetchall()

PM10Sens1, = cursor.execute("SELECT sensor1 FROM pm10 ORDER BY rowid DESC LIMIT 1").fetchall()
PM10Sens2, = cursor.execute("SELECT sensor2 FROM pm10 ORDER BY rowid DESC LIMIT 1").fetchall()
PM10Sensavg, = cursor.execute("SELECT avg FROM pm10 ORDER BY rowid DESC LIMIT 1").fetchall()

NoxSens1, = cursor.execute("SELECT sensor1 FROM nox ORDER BY rowid DESC LIMIT 1").fetchall()
NoxSens2, = cursor.execute("SELECT sensor2 FROM nox ORDER BY rowid DESC LIMIT 1").fetchall()
NoxSensavg, = cursor.execute("SELECT avg FROM nox ORDER BY rowid DESC LIMIT 1").fetchall()

VocSens1, = cursor.execute("SELECT sensor1 FROM voc ORDER BY rowid DESC LIMIT 1").fetchall()
VocSens2, = cursor.execute("SELECT sensor2 FROM voc ORDER BY rowid DESC LIMIT 1").fetchall()
VocSensavg, = cursor.execute("SELECT avg FROM voc ORDER BY rowid DESC LIMIT 1").fetchall()

tempSens1, = cursor.execute("SELECT sensor1 FROM temp ORDER BY rowid DESC LIMIT 1").fetchall()
tempSens2, = cursor.execute("SELECT sensor2 FROM temp ORDER BY rowid DESC LIMIT 1").fetchall()
tempSensavg, = cursor.execute("SELECT avg FROM temp ORDER BY rowid DESC LIMIT 1").fetchall()

humiditySens1, = cursor.execute("SELECT sensor1 FROM humidity ORDER BY rowid DESC LIMIT 1").fetchall()
humiditySens2, = cursor.execute("SELECT sensor2 FROM humidity ORDER BY rowid DESC LIMIT 1").fetchall()
humiditySensavg, = cursor.execute("SELECT avg FROM humidity ORDER BY rowid DESC LIMIT 1").fetchall()

#publish variables
data=f'''{UTC}#{Aqi10}#{Aqi2p5}
#{PM1Sens1}#{PM1Sens2}#{PM1Sensavg}
#{PM2p5Sens1}#{PM2p5Sens2}#{PM2p5Sensavg}
#{PM4Sens1}#{PM4Sens2}#{PM4Sensavg}
#{PM10Sens1}#{PM10Sens2}#{PM10Sensavg}
#{NoxSens1}#{NoxSens2}#{NoxSensavg}
#{VocSens1}#{VocSens2}#{VocSensavg}
#{tempSens1}#{tempSens2}#{tempSensavg}
#{humiditySens1}#{humiditySens2}#{humiditySensavg}'''

client.publish('testTopic',data,2)


client.loop_stop()
client.disconnect()
print("end mqtt")