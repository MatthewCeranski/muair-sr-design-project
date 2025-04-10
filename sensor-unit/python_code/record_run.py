################################################################ BLOCK 1 ######################################################################

## Database Commands
import time
import math
import sqlite3
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import DFRobot_I2C_Multiplexer
import i2clcd
from AQIPython import calculate_aqi

################################################################ BLOCK 2 #####################################################################
#create database
conn = sqlite3.connect("MUAIRtestdatabase") #connect to database if it exists
print(conn.total_changes) #print confirmation (0 if connected)
cursor = conn.cursor() #define cursor function





## Sensor Driver Commands
from sensirion_i2c_driver import I2cConnection, LinuxI2cTransceiver
from sensirion_i2c_sen5x import Sen5xI2cDevice

I2CMultiAddr = 0x70     #I2C Multiplexer addr
I2CMulti = DFRobot_I2C_Multiplexer.DFRobot_I2C_Multiplexer(I2CMultiAddr)


for i in range(1):
    I2CMulti.select_port(6)
    with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver:
        device = Sen5xI2cDevice(I2cConnection(i2c_transceiver))#connection
        #print(device.slave_address)
        #print(device.connection)
        device.start_measurement()
        values = device.read_measured_values()
        pm1sens1 = values.mass_concentration_1p0.physical
        pm25sens1 = values.mass_concentration_2p5.physical
        pm4sens1 = values.mass_concentration_4p0.physical
        pm10sens1 = values.mass_concentration_10p0.physical
        humiditysens1 = values.ambient_humidity.percent_rh
        tempsens1 = values.ambient_temperature.degrees_celsius
        vocsens1 = values.voc_index.scaled
        noxsens1 = values.nox_index.scaled
        print('sensor 1 measured')
        time.sleep(0.1)


    I2CMulti.select_port(5)
    with LinuxI2cTransceiver('/dev/i2c-1') as i2c_transceiver:
        device = Sen5xI2cDevice(I2cConnection(i2c_transceiver))#connection#connection
        #print(device.slave_address)
        #print(device.connection)

        device.start_measurement()
        values = device.read_measured_values()
        pm1sens2 = values.mass_concentration_1p0.physical
        pm25sens2 = values.mass_concentration_2p5.physical
        pm4sens2 = values.mass_concentration_4p0.physical
        pm10sens2 = values.mass_concentration_10p0.physical
        humiditysens2 = values.ambient_humidity.percent_rh
        tempsens2 = values.ambient_temperature.degrees_celsius
        vocsens2 = values.voc_index.scaled
        noxsens2 = values.nox_index.scaled
        print('sensor 2 measured')
        time.sleep(0.1)

    UTC=datetime.now()
    #avearge and adjustments here
    pm10avg= sum([pm10sens1, pm10sens2])/2
    pm25avg= sum([pm25sens1, pm25sens2])/2
    pm4avg= sum([pm4sens1, pm4sens2])/2
    pm1avg= sum([pm1sens1, pm1sens2])/2
    noxavg= sum([noxsens1, noxsens2])/2
    vocavg= sum([vocsens1, vocsens2])/2
    humidityavg= sum([humiditysens1, humiditysens2])/2
    tempavg= sum([tempsens1, tempsens2])/2

    #create tuples to insert
    pm10data= (UTC, pm10sens1, pm10sens2, pm10avg)
    pm25data=(UTC, pm25sens1, pm25sens2, pm25avg)
    pm4data=(UTC, pm4sens1, pm4sens2, pm4avg)
    pm1data=(UTC, pm1sens1, pm1sens2, pm1avg)
    noxdata=(UTC, noxsens1, noxsens2, noxavg)
    vocdata=(UTC, vocsens1, vocsens2, vocavg)
    humiditydata=(UTC, humiditysens1, humiditysens2, humidityavg)
    tempdata=(UTC, tempsens1, tempsens2, tempavg)
    #insert into tables

    cursor.execute("INSERT INTO pm10 VALUES (?, ?, ?, ?)", pm10data)
    cursor.execute("INSERT INTO pm4 VALUES (?, ?, ?, ?)", pm4data)
    cursor.execute("INSERT INTO pm2p5 VALUES (?, ?, ?, ?)", pm25data)
    cursor.execute("INSERT INTO pm1 VALUES (?, ?, ?, ?)", pm1data)
    cursor.execute("INSERT INTO nox VALUES (?, ?, ?, ?)", noxdata)
    cursor.execute("INSERT INTO voc VALUES (?, ?, ?, ?)", vocdata)
    cursor.execute("INSERT INTO humidity VALUES (?, ?, ?, ?)", humiditydata)
    cursor.execute("INSERT INTO temp VALUES (?, ?, ?, ?)", tempdata)
    conn.commit()
    print ("record inserted")
print("end")