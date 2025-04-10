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

res = cursor.execute("SELECT avg FROM pm2p5 ORDER BY rowid DESC LIMIT 40").fetchall()

#print(res)
digits = 5
rawpm2p5 = statistics.mean(res)

AQI25 = calculate_aqi('US','PM25', rawpm2p5,"ug/m3")

def truncate(AQI10, digits) -> float:
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(AQI25).split('.')[1])
    if nbDecimals <= 3:
        return AQI25
    stepper = 10.0 ** 3
    return math.trunc(stepper * AQI25) / stepper

AQI25trunc = truncate(AQI25, digits)

UTC =datetime.now()
aqi25param = (UTC, AQI25trunc)

cursor.execute("INSERT INTO aqi25 VALUES (?, ?)", aqi25param)
conn.commit()
print("end")
