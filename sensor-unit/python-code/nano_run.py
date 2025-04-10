import sqlite3
import i2clcd
import time
import pandas
import DFRobot_I2C_Multiplexer

#fetch single values from end of database

#connect to database, pull latest numbers
conn=sqlite3.connect('MUAIRtestdatabase', check_same_thread=False)
cursor=conn.cursor()
#fetch temp
cursor.execute("SELECT avg FROM temp ORDER BY rowid DESC LIMIT 1")
tempvalue,=cursor.fetchone()
tempvalue = round(tempvalue,1)

#fetch RH
cursor.execute("SELECT avg FROM temp ORDER BY rowid DESC LIMIT 1")
rhvalue,=cursor.fetchone()
rhvalue = round(rhvalue,1)

#fetch pm1
cursor.execute("SELECT avg FROM pm1 ORDER BY rowid DESC LIMIT 1")
pm1value,=cursor.fetchone()
if pm1value < 100:
    pm1value = round(pm1value,1)
elif pm1value >= 100:
    pm1value = round(pm1value)


#fetch pm2.5
cursor.execute("SELECT avg FROM pm2p5 ORDER BY rowid DESC LIMIT 1")
pm25value,=cursor.fetchone()
if pm25value < 100:
    pm25value = round(pm25value,1)
elif pm25value >= 100:
    pm25value = round(pm25value)

#fetch pm4
cursor.execute("SELECT avg FROM pm4 ORDER BY rowid DESC LIMIT 1")
pm4value,=cursor.fetchone()
if pm4value < 100:
    pm4value = round(pm4value,1)
elif pm4value >= 100:
    pm4value = round(pm4value)

#fetch 10
cursor.execute("SELECT avg FROM pm10 ORDER BY rowid DESC LIMIT 1")
pm10value,=cursor.fetchone()
if pm10value < 100:
    pm10value = round(pm10value,1)
elif pm10value >= 100:
    pm10value = round(pm10value)

#fetch aqi
cursor.execute("SELECT aqi10 FROM aqi10 ORDER BY rowid DESC LIMIT 1")
aqi10value,=cursor.fetchone()
cursor.execute("SELECT aqi25 FROM aqi25 ORDER BY rowid DESC LIMIT 1")
aqi25value,=cursor.fetchone()



if aqi10value > aqi25value:
    aqidisplay = round(aqi10value)
elif aqi25value > aqi10value:
    aqidisplay = round(aqi25value)
elif aqi25value == aqi10value:
    aqidisplay = round(aqi10value)
#have 8 on top
#have 16 on bottom
if aqidisplay <= 50:
    levelaqi = 'Good' #4
    action1 = 'Optimal air!'
    action2 = 'Get Outside Now!'
elif 50 < aqidisplay <= 100:
    levelaqi = 'Moderate' #8
    action1 = 'Moderate Air'
    action2 = 'Monitor AQI!'
elif 100 < aqidisplay <= 150:
    levelaqi = 'Sensitive' #9
    action1 = 'Moderate air'
    action2 = 'Limit Exertion'
elif 150 < aqidisplay <= 200:
    levelaqi = 'Unhealthy' #9
    action1 = 'Poor Air'
    action2 = 'Limit Time Out'
elif 200 < aqidisplay <= 300:
    levelaqi = 'Very Unhealthy' #14
    action1 = '*Bad Air!*'
    action2 = 'Be Careful'
elif aqidisplay > 300:
    levelaqi = 'Dangerous' #9
    action1 = 'Hazardous!'
    action2 = '*Stay Indoors*'


I2CMultiAddr = 0x70     #I2C Multiplexer addr
I2CMulti = DFRobot_I2C_Multiplexer.DFRobot_I2C_Multiplexer(I2CMultiAddr)
I2CMulti.select_port(4)
#export to LCD
# in this loop we can have 'if x is > y, display "x high, stay inside"
lcd = i2clcd.i2clcd(i2c_bus=1, i2c_addr=0x27, lcd_width=16)
while True:
    lcd.init()
    # fill a line by the text
    lcd.clear()
    lcd.move_cursor(0,0)
    lcd.print(f'P1 {pm1value}')
    lcd.move_cursor(1,0)
    lcd.print(f'P4 {pm4value}')
    lcd.move_cursor(0,8)
    lcd.print(f'P25 {pm25value}')
    lcd.move_cursor(1,8)
    lcd.print(f'P10 {pm10value}')
    time.sleep(5)

    lcd.clear()
    lcd.move_cursor(0,0)
    lcd.print(f'RH {rhvalue}')
    lcd.move_cursor(1,0)
    lcd.print(f'Temp {tempvalue}')
    time.sleep(5)

    lcd.clear()
    lcd.move_cursor(0,0)
    lcd.print_line(f'AQI {aqidisplay}', line=0, align='Center')
    lcd.move_cursor(1,0)
    #lcd.print(f'Level is {levelaqi}')
    time.sleep(5)

    lcd.clear()
    lcd.move_cursor(0,0)
    lcd.print_line(f'{action1}', line=0, align='Center')
    lcd.move_cursor(1,0)
    lcd.print_line(f'{action2}', line=1, align='Center')
    time.sleep(5)