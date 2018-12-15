import RPi.GPIO as GPIO
import time
import datetime
import subprocess
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Handler
import threading
# from lcd import lcd

bot = telegram.Bot(token='624744889:AAGawjqx9eHRIG_5m_RboOg1UmLslSme2L4')
updater = Updater("624744889:AAGawjqx9eHRIG_5m_RboOg1UmLslSme2L4")

    # Get the dispatcher to register handlers
# on different commands - answer in Telegram
ids = set()

def start():
    add_id = update.message.chat.id
    print(add_id)
    ids.add(add_id)
    update.message.reply_text(text = 'Hi!')


dt_now = lambda : datetime.datetime.now()

led_pin = 11    # pin11
button_pin = 10

# max_update_id = 0
# def bot_get_updates():
#     for update in bot.get_updates(max_update_id):

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(led_pin, GPIO.OUT)   # Set led_pin's mode is output
    GPIO.output(led_pin, GPIO.HIGH) # Set led_pin high(+3.3V) to turn on led
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main():
    runOnce = True
    while True:
        if GPIO.input(button_pin) == GPIO.HIGH and not runOnce:
            runOnce = True
            OnButtonDown()
        elif GPIO.input(button_pin) == GPIO.LOW and runOnce:
            runOnce = False
            GPIO.output(led_pin, GPIO.LOW) # led off

def OnButtonDown():
    for update in bot.get_updates():
        if update.message.text == '/emil_loh':
            ids.add(update.message.chat_id)
            bot.send_chat_action(update.message.chat_id, 'upload_photo')
    GPIO.output(led_pin, GPIO.HIGH)  # led on
    subprocess.call(["python3", "lcd.py", "proccessing..."])
    print("A picture is being taken...")
    time = dt_now()
    file_name = 'photos/guest{time:%Y%m%d_%H%M%S}.jpg'.format(time=time)

    subprocess.call(['fswebcam', file_name])
    print("There is a guest waiting for your response!")
   
    for id in ids:
        bot.send_photo(chat_id=id, photo=open(file_name, 'rb'))
        # bot.send_message(chat_id=id, text="I'm sorry Dave I'm afraid I can't do that.")

    subprocess.call(["python3", "lcd.py", "sent!!!"])

def destroy():
    GPIO.output(led_pin, GPIO.LOW)   # led off
    GPIO.cleanup()                  # Release resource
    print("\n\n* Program is terminated!")

if __name__ == '__main__': 
    print("* Program is running.\n")    # Program start from here
    setup()
    try:
        main()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()
