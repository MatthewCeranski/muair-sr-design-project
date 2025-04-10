import time
import math
import sqlite3
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))


################################################################ BLOCK 2 #####################################################################
#create database
conn = sqlite3.connect("MUAIRtestdatabase") #connect to database if it exists
print(conn.total_changes) #print confirmation (0 if connected)
cursor = conn.cursor() #define cursor function


cursor.execute("DROP TABLE IF EXISTS pm10")
cursor.execute("DROP TABLE IF EXISTS pm4")
cursor.execute("DROP TABLE IF EXISTS pm2p5")
cursor.execute("DROP TABLE IF EXISTS pm1")
cursor.execute("DROP TABLE IF EXISTS nox")
cursor.execute("DROP TABLE IF EXISTS voc")
cursor.execute("DROP TABLE IF EXISTS humidity")
cursor.execute("DROP TABLE IF EXISTS temp")
cursor.execute("DROP TABLE IF EXISTS aqi25")
cursor.execute("DROP TABLE IF EXISTS aqi10")


#create tables blank
cursor.execute("CREATE TABLE pm10 (time REAL, sensor1 REAL, sensor2 REAL, avg REAL)")
print("Table pm10 created")
cursor.execute("CREATE TABLE pm4 (time REAL, sensor1 REAL, sensor2 REAL, avg REAL)")
print("Table pm4 created")
cursor.execute("CREATE TABLE pm2p5 (time REAL, sensor1 REAL, sensor2 REAL, avg REAL)")
print("Table pm2p5 created")
cursor.execute("CREATE TABLE pm1 (time REAL, sensor1 REAL, sensor2 REAL, avg REAL)")
print("Table pm1 created")
cursor.execute("CREATE TABLE nox (time REAL, sensor1 REAL, sensor2 REAL, avg REAL)")
print("Table nox created")
cursor.execute("CREATE TABLE voc (time REAL, sensor1 REAL, sensor2 REAL, avg REAL)")
print("Table voc created")
cursor.execute("CREATE TABLE humidity (time REAL, sensor1 REAL, sensor2 REAL, avg REAL)")
print("Table humidity created")
cursor.execute("CREATE TABLE temp (time REAL, sensor1 REAL, sensor2 REAL, avg REAL)")
print("Table temp created")
cursor.execute("CREATE TABLE aqi25 (time REAL, aqi25 REAL)")
print("Table aqi25 created")
cursor.execute("CREATE TABLE aqi10 (time REAL, aqi10 REAL)")
print("Table aqi10 created")

conn.commit()