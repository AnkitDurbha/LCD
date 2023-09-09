from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import Freenove_DHT as DHT
DHTPin = 11     # Defining the pin for the temperature sensor

def get_temp():
    dht = DHT.DHT(DHTPin)   # Creating a class object for the temperature sensor
    for i in range(15):
        chk = dht.readDHT11()
        if (chk is dht.DHTLIB_OK):
            break
        sleep(0.1)
    f_temp = 0
    c_temp = dht.temperature    # Setting the temperature value equal to variable c_temp
    f_temp = (c_temp * (9/5)) + 32  # Converting the temperature to fahrenheight
    rounded_num = round(f_temp, 2)  # Rounding the temperature to 2 decimal places
    return "  Temp : " + str(rounded_num)

def get_time_now():     # get system time
    return datetime.now().strftime(' Time : ' + '%-I:%M %p')    # Getting the current time

def loop():
    mcp.output(3,1)     # Turn on LCD backlight
    lcd.begin(16,2)     # Set number of LCD lines and columns
    while(True):
        #lcd.clear()
        lcd.setCursor(0,0)
        lcd.message(get_temp()+'\n')    # Display the temperature
        lcd.message(get_time_now())    # Display the time
        sleep(1)

def destroy():
    lcd.clear()

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(PCF8574A_address)
    except:
        print ('I2C Address Error !')
        exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        destroy()