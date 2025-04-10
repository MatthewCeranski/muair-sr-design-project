import time
import math
import sqlite3
from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
import re

from AQIPython import calculate_aqi
from itertools import chain
import statistics



conn = sqlite3.connect("MUAIRtestdatabase") #connect to database if it exists
conn.row_factory = lambda cursor, row: row[0]
cursor = conn.cursor() #define cursor function

res = cursor.execute("SELECT avg FROM pm10 ORDER BY rowid DESC LIMIT 40").fetchall()

#print(res)
digits = 5
rawpm10 = statistics.mean(res)

AQI10 = calculate_aqi('US','PM10', rawpm10,"ug/m3")

def truncate(AQI10, digits) -> float:
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(AQI10).split('.')[1])
    if nbDecimals <= 3:
        return AQI10
    stepper = 10.0 ** 3
    return math.trunc(stepper * AQI10) / stepper

AQI10trunc = truncate(AQI10, digits)

UTC =datetime.now()
aqi10param = (UTC, AQI10trunc)

cursor.execute("INSERT INTO aqi10 VALUES (?, ?)", aqi10param)
conn.commit()

print("end")