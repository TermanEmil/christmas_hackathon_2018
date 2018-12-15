import RPi.GPIO as GPIO
import datetime
import subprocess
import telegram
import threading
import random
import consts

from time import sleep
from on_button_down import OnButtonDown
from photo_ops import send_photo, take_photo
from telegram_update_thread import TelegramUpdateThread
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Handler

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)               # Numbers GPIOs by physical location
    GPIO.setup(consts.led_pin, GPIO.OUT)   # Set led_pin's mode is output
    GPIO.output(consts.led_pin, GPIO.HIGH) # Set led_pin high(+3.3V) to turn on led
    GPIO.setup(consts.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def destroy():
    GPIO.output(consts.led_pin, GPIO.LOW)      # led off
    GPIO.cleanup()                             # Release resource
    print("\n\n* Program is terminated!")

def main():
    runOnce = True
    while True:
        if GPIO.input(consts.button_pin) == GPIO.HIGH and not runOnce:
            runOnce = True
            OnButtonDown(bot, ids)
        elif GPIO.input(consts.button_pin) == GPIO.LOW and runOnce:
            runOnce = False
            GPIO.output(consts.led_pin, GPIO.LOW)  # led off

if __name__ == '__main__': 
    print("* Program is running.\n")

    bot = telegram.Bot(token='624744889:AAGawjqx9eHRIG_5m_RboOg1UmLslSme2L4')
    ids = set()

    telegram_update = TelegramUpdateThread(bot, ids)
    telegram_update.start()
    setup()
    
    try:
        main()
    except KeyboardInterrupt:
        # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
