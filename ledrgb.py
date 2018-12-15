import sys, time
import RPi.GPIO as GPIO

redPin = 29
greenPin = 31
bluePin = 32
buttonPin = 10

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(redPin, GPIO.OUT)
    GPIO.setup(greenPin, GPIO.OUT)
    GPIO.setup(bluePin, GPIO.OUT)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def turnOn(pin1, pin2=None, pin3=None):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(redPin, GPIO.OUT)
    GPIO.setup(greenPin, GPIO.OUT)
    GPIO.setup(bluePin, GPIO.OUT)

    GPIO.output(pin1, GPIO.HIGH)
    if pin2:
        GPIO.output(pin2, GPIO.HIGH)
    if pin3:
        GPIO.output(pin3, GPIO.HIGH)

def turnOff(pin1, pin2=None, pin3=None):
    GPIO.output(pin1, GPIO.LOW)
    if pin2:
        GPIO.output(pin2, GPIO.LOW)
    if pin3:
        GPIO.output(pin3, GPIO.LOW)

def destroy():
    turnOff(redPin, greenPin, bluePin)
    GPIO.cleanup()
    print("\n* Program is terminated!")

def main():
    runOnce = True
    while True:
        if GPIO.input(buttonPin) == GPIO.HIGH and not runOnce:
            runOnce = True
            OnButtonDown()
        elif GPIO.input(buttonPin) == GPIO.LOW and runOnce:
            print("Button Up")
            runOnce = False
            turnOff(redPin, greenPin, bluePin)

def OnButtonDown():
    print("Button Down!")
    turnOn(redPin, greenPin, bluePin)


if __name__ == '__main__':
    print("* Program is running.\n")
    setup()
    try:
        main()
    except KeyboardInterrupt:
        destroy()