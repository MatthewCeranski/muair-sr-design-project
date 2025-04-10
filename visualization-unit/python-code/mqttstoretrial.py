import sys
import os
import paho.mqtt.client as mqtt
import time
import sqlite3

#broker information
serv='10.162.25.103'
username= "muairvis"
password= "muairvis"

#define callbacks
def on_connect(client, userdata, flags, rc, properties=None):
    print("connected", str(rc))
    client.subscribe("testTopic",2)

def on_message(mosq, obj, msg):
    msg = msg.payload.decode("utf-8")
    #print(msg)
    msg_list = msg.split("#")
    UTC = msg_list[0]
    Aqi10= msg_list[1]
    Aqi2p5= msg_list[2]
    PM1Sens1= msg_list[3]
    PM1Sens2= msg_list[4]
    PM1avg= msg_list[5]
    PM2p5Sens1= msg_list[6]
    PM2p5Sens2= msg_list[7]
    PM2p5avg= msg_list[8]
    PM4Sens1= msg_list[9]
    PM4Sens2= msg_list[10]
    PM4avg= msg_list[11]
    PM10Sens1= msg_list[12]
    PM10Sens2= msg_list[13]
    PM10avg= msg_list[14]
    NoxSens1= msg_list[15]
    NoxSens2= msg_list[16]
    Noxavg= msg_list[17]
    VocSens1= msg_list[18]
    VocSens2= msg_list[19]
    Vocavg= msg_list[20]
    tempSens1= msg_list[21]
    tempSens2= msg_list[22]
    tempavg= msg_list[23]
    humiditySens1= msg_list[24]
    humiditySens2= msg_list[25]
    humidityavg= msg_list[26]

    conn = sqlite3.connect("MUAIRtestdatabase")
    cursor = conn.cursor()

    #create tuples to insert
    pm10data= (UTC, PM10Sens1, PM10Sens2, PM10avg)
    pm25data=(UTC, PM2p5Sens1, PM2p5Sens2, PM2p5avg)
    pm4data=(UTC, PM4Sens1, PM4Sens2, PM4avg)
    pm1data=(UTC, PM1Sens1, PM1Sens2, PM1avg)
    noxdata=(UTC, NoxSens1, NoxSens2, Noxavg)
    vocdata=(UTC, VocSens1, VocSens2, Vocavg)
    humiditydata=(UTC, humiditySens1, humiditySens2, humidityavg)
    tempdata=(UTC, tempSens1, tempSens2, tempavg)
    aqi10data= (UTC, Aqi10)
    aqi2p5data=(UTC, Aqi2p5)
    #insert into tables



    cursor.execute("INSERT INTO pm10 VALUES (?, ?, ?, ?)", pm10data)
    cursor.execute("INSERT INTO pm4 VALUES (?, ?, ?, ?)", pm4data)
    cursor.execute("INSERT INTO pm2p5 VALUES (?, ?, ?, ?)", pm25data)
    cursor.execute("INSERT INTO pm1 VALUES (?, ?, ?, ?)", pm1data)
    cursor.execute("INSERT INTO nox VALUES (?, ?, ?, ?)", noxdata)
    cursor.execute("INSERT INTO voc VALUES (?, ?, ?, ?)", vocdata)
    cursor.execute("INSERT INTO humidity VALUES (?, ?, ?, ?)", humiditydata)
    cursor.execute("INSERT INTO temp VALUES (?, ?, ?, ?)", tempdata)
    cursor.execute("INSERT INTO aqi10 VALUES (?, ?)", aqi10data)
    cursor.execute("INSERT INTO aqi25 VALUES (?, ?)", aqi2p5data)
    conn.commit()
    print(F'Data inserted for {UTC}')
    print(pm10data)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_message = on_message
client.on_connect = on_connect

client.connect(serv, 1883, 60)


client.loop_forever()
client.loop_stop()