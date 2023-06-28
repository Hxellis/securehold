import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint
import tkinter

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



##########WINDOW###########
window = tkinter.Tk()
window.geometry("600x400")

#screens
rfidScreen = tkinter.Frame(window)

welcomeScreen = tkinter.Frame(window)
fingerprintScreen = tkinter.Frame(window)
lockerUnlockScreen = tkinter.Frame(window)


def switchScreen(forgetScreen, showScreen):
    forgetScreen.place_forget()
    showScreen.place(relx=0.5, rely=0.5, anchor="c")
    
def buzz(timeout):
	GPIO.output(buzzer,GPIO.HIGH)
	sleep(timeout)	
	GPIO.output(buzzer,GPIO.LOW)
    
def loop():
	rfidScreenText = tkinter.Label(rfidScreen, text="Please scan your RFID CARD", font=("Arial", 30))
	rfidScreenText.grid(column=0, row=0)
	rfidScreen.place(relx=0.5, rely=0.5, anchor="c")
	window.update()
	id, Tag = read.read()
	id = str(id)
	Tag = Tag.replace(" ", "")
	
	if id == Tag_ID:
		sampleText = "12345"
		rfidScreen.place_forget()
		welcomeScreenText = tkinter.Label(welcomeScreen, text="Welcome " + Tag, font=("Arial", 30))
		welcomeScreenText.grid(column=0, row=0)
		welcomeScreen.place(relx=0.5, rely=0.5, anchor="c")
		window.update()
		
		buzz(0.5)
		
		window.after(3000, 0)
		
		welcomeScreen.place_forget()
		fingerprintScreenText = tkinter.Label(fingerprintScreen, text="Please scan your face \n or put your fingerprint", font=("Arial", 30))
		fingerprintScreenText.grid(column=0, row=0)
		fingerprintScreen.place(relx=0.5, rely=0.5, anchor="c")
		window.update()
		if get_fingerprint():

			GPIO.output(RELAY_PIN, GPIO.LOW)
			fingerprintScreen.place_forget()
			lockerUnlockScreenText = tkinter.Label(lockerUnlockScreen, text="Locker unlocked", font=("Arial", 30))
			lockerUnlockScreenText.grid(column=0, row=0)
			window.update()
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

	GPIO.cleanup()
	window.after(100, loop)
	
	
##fsadfsf		
window.after(100,loop)		
window.mainloop()


