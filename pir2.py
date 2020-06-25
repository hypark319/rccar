import RPi.GPIO as GPIO
import time
​
GPIO.setmode(GPIO.BCM)
​
pirPin = 23
GPIO.setup(pirPin, GPIO.IN)
​

def loop():
    while True:

        if GPIO.input(pirPin) == GPIO.LOW:

            print "Motion detected!"

        else:

            print "No motion"

        time.sleep(0.2)


try:
    loop()
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()