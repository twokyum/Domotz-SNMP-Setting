#!/usr/bin/python2
import socket
import serial
import logging
import logging.handlers
from logging.handlers import TimedRotatingFileHandler
import time

ser = serial.Serial('/dev/ttyAMA0', 38400)

#Directories
base_dir='/usr/local/bin/'
temptxt_file = base_dir + 'read_temp.txt' 
testPath='/usr/local/bin/Logging_Data/temperature.log'


#Logger, Handler Setup
handler = TimedRotatingFileHandler(testPath, when="midnight", interval=1)
    #s=second
    #m=minutes
    #h=hours
    #d=days
    #W0-W6 = Weekdays
    #midnight = roll over at midnight



def write_timed_rotation_log(path, cel, fah, domotz_id):
    
    name = "MonIT ID[" + domotz_id + "]-"+socket.gethostname()
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(name)s %(asctime)s %(message)-8s'))
    logger.addHandler(handler)
    logger.info("Temperature= %s°C  %s°F",cel, str(fah))
    #handler.suffix='%Y%m%d.log'


def read_lines():
    
    line = ser.readline()

    line = line[:-2]
    line = line.decode('utf-8')
    Z = line.split(",")
  

  
    #Variable Set and Conversion
    domotz_id = Z[0]
    Celcius = Z[4]
    Fahrenheit = round(float(Z[4])*1.8, 1)+32
    
    #Pass values to the function
    write_timed_rotation_log(testPath, Celcius, Fahrenheit, domotz_id)
    
    #Test PRint
    print(Z[4])
    print(Fahrenheit)

    return(Z[4])




#Repeats reading lines until interruption 
def serialReading():
    
    try:
        while 1:
            #time.sleep(15)
            time.sleep(600)
            temp = read_lines()
    except KeyboardInterrupt:
               ser.close()
    return temp




serialReading()

