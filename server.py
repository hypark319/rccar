import bluetooth
import RPi.GPIO as GPIO  # calling for header file which helps in using GPIOs of PI


# RC Code

import RPi.GPIO as GPIO
from time import sleep

STOP = 0
FORWARD = 1
BACKWORD = 2

CH1 = 0
CH2 = 1

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

ENA = 26  # 37 pin
ENB = 0  # 27 pin

IN1 = 19  # 35 pin
IN2 = 13  # 33 pin
IN3 = 6  # 31 pin
IN4 = 5  # 29 pin



def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm = GPIO.PWM(EN, 100)
    pwm.start(0)
    return pwm


def setMotorContorl(pwm, INA, INB, speed, stat):
    pwm.ChangeDutyCycle(speed)
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
    elif stat == BACKWORD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)


def setMotor(ch, speed, stat):
    if ch == CH1:
        setMotorContorl(pwmA, IN1, IN2, speed, stat)
    else:
        setMotorContorl(pwmB, IN3, IN4, speed, stat)






# Below Server code

LED = 21

GPIO.setmode(GPIO.BCM)  # programming the GPIO by BCM pin numbers. (like PIN40 as GPIO21)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)  # initialize GPIO21 (LED) as an output Pin
GPIO.output(LED, 0)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(1)

client_socket, address = server_socket.accept()
print "Accepted connection from ", address
while 1:

    data = client_socket.recv(1024)
    print "Received: %s" % data
    if (data == "0"):  # if '0' is sent from the Android App, turn OFF the LED
        print ("GPIO 21 LOW, LED OFF")
        setMotor(CH1, 100, FORWARD)
        setMotor(CH2, 100, FORWARD)
    if (data == "1"):  # if '1' is sent from the Android App, turn OFF the LED
        print ("GPIO 21 HIGH, LED ON")
        setMotor(CH1, 100, BACKWORD)
        setMotor(CH2, 100, BACKWORD)
    if (data == "q"):
        setMotor(CH1, 80, STOP)
        setMotor(CH2, 80, STOP)
        print ("Quit")
        break

client_socket.close()
server_socket.close()