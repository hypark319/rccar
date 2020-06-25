import bluetooth
import RPi.GPIO as GPIO
import time

# RC Code

STOP = 0
FORWARD = 1
BACKWORD = 2

CH1 = 0
CH2 = 1

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

ENA = 26  # board 37 pin
ENB = 0  # board 27 pin

IN1 = 19  # board 35 pin
IN2 = 13  # board 33 pin
IN3 = 6  # board 31 pin
IN4 = 5  # board 29 pin

pirPin = 23 # board 16 pin, motion sensor



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

def loop():
    while True:

        if GPIO.input(pirPin) == GPIO.LOW:

            print "Motion detected!"

        else:

            print "No motion"

        time.sleep(0.2)






# Below Server code



GPIO.setmode(GPIO.BCM)  # programming the GPIO by BCM pin numbers. (like PIN40 as GPIO21)
GPIO.setwarnings(False)


pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(1)

client_socket, address = server_socket.accept()
print "Accepted connection from ", address
try:
    loop()
    while (1):
        data = client_socket.recv(1024)
        print "Received: %s" % data
        if (data == "0"):  # if '0' is sent from the Android App, turn OFF the LED
            setMotor(CH1, 50, FORWARD)
            setMotor(CH2, 50, FORWARD)
        if (data == "1"):  # if '1' is sent from the Android App, turn OFF the LED
            setMotor(CH1, 50, BACKWORD)
            setMotor(CH2, 50, BACKWORD)
        if (data == "r"):  # if '0' is sent from the Android App, turn OFF the LED
            setMotor(CH1, 50, FORWARD)
            setMotor(CH2, 20, FORWARD)
        if (data == "l"):  # if '0' is sent from the Android App, turn OFF the LED
            setMotor(CH1, 20, FORWARD)
            setMotor(CH2, 50, FORWARD)
        if (data == "q"):
            setMotor(CH1, 80, STOP)
            setMotor(CH2, 80, STOP)
        if (data == "e"):
            setMotor(CH1, 80, STOP)
            setMotor(CH2, 80, STOP)
            break

client_socket.close()
server_socket.close()