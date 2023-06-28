import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint

#########BUZZER########
buzzer = 26

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzer,GPIO.OUT)
##########RELAY###########
RELAY_PIN = 19

GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.HIGH)
#######FINGERPRINT##############
import serial
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    
    return True
    




############RFID###########
Tag_ID = "698885712740"

read = SimpleMFRC522()


try:
    
    print("Please scan your RFID CARD")
    id, Tag = read.read()
    id = str(id)
    
    if id == Tag_ID:
        
        print("Welcome" + " " + Tag)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)
        #sleep(3)
        print("Please scan your face or put your fingerprint")
        
        if get_fingerprint():



            GPIO.output(RELAY_PIN, GPIO.LOW)
            print("Locker unlocked")
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW) 
            sleep(5)
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            

            
        else:
            print("Fingerprint not authorised")
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW) 
    
    else:
        print("not registered user")
        
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzzer,GPIO.LOW)    
    
         
finally:
    GPIO.cleanup()