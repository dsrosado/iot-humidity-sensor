#!/usr/bin/python
from datetime import datetime
import MySQLdb
import RPi.GPIO as GPIO
import dht11
import time 

def subedatos(temp, humi):
        sensor = 1
        fecha_dato = datetime.now()
        dato01 = temp
        dato02 = humi
        print("Fecha: %s" % fecha_dato)
        print("Temperature: %d C" % temp)
        print("Humidity: %d %%" % humi)

        # Push data into SQL
        sql = "INSERT INTO sensordata (sensor, fecha_dato, dato01, dato02) VALUES (%s, %s, %s, %s)"

        try:

            # Execute the SQL command
            data = (sensor, fecha_dato, dato01, dato02)
            cursor.execute (sql,data)
            # Commit your changes in the database
            db.commit()

        except MySQLdb.Error, e:
            print("Something went wrong: {}".format(e))
            # Rollback in case there is any error
            db.rollback()

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Connect to MySQL: los datos deben ser los de tu servidor y user/passw de tu BD
servername = "el tuyo";
username = "el tuyo";
password = "el tuyo";
dbname = "iothings";
db = MySQLdb.connect(servername,username,password,dbname)
cursor = db.cursor()

while True:
    # read data using pin 4
    instance = dht11.DHT11(pin = 4)
    result = instance.read()

    if result.is_valid():
        subedatos(result.temperature, result.humidity)

    else:
        print("...")
    
    # Wait 0.1 of a second, para darle un respiro a la CPU
    time.sleep(1)
