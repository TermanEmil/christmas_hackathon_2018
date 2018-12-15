import RPi.GPIO as GPIO
import time
import datetime
import subprocess
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Handler
import threading
import random
# from lcd import lcd

bot = telegram.Bot(token='624744889:AAGawjqx9eHRIG_5m_RboOg1UmLslSme2L4')
updater = Updater("624744889:AAGawjqx9eHRIG_5m_RboOg1UmLslSme2L4")

    # Get the dispatcher to register handlers
# on different commands - answer in Telegram
ids = set()
guest_texts = [
 "Au venit uratori",
 "Aveti oaspeti",
 "Aho aho copii si frati..."
]
# def start():
#     add_id = update.message.chat.id
#     print(add_id)
#     ids.add(add_id)
#     update.message.reply_text(text = 'Hi!')


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

def take_photo():
    time = dt_now()
    file_name = 'photos/guest{time:%Y%m%d_%H%M%S}.jpg'.format(time=time)

    subprocess.call(['fswebcam', '--no-banner', file_name])
    return file_name

def send_photo(file_name, caption=None):
    for chat_id in ids:
        bot.send_photo(chat_id=chat_id, photo=open(file_name, 'rb'), caption=caption)

def main():
    max_update_id = 0
    runOnce = True
    while True:
        for update in bot.get_updates(max_update_id + 1):
            max_update_id = max(max_update_id, update.update_id)
            if not update.message.text:
                break
            if update.message.text == '/start' and not update.message.chat_id in ids:
                ids.add(update.message.chat_id)
                bot.send_message(chat_id = update.message.chat_id, text = "Hi!")
            elif update.message.chat_id in ids:
                if update.message.text == '/stop':
                    ids.remove(update.message.chat_id)
                elif update.message.text.startswith('/send'):
                    _, _, text_to_send = update.message.text.partition(' ')
                    subprocess.call(["python3", "lcd.py", text_to_send[:16] + '\n' + text_to_send[16:32]])
                elif update.message.text.startswith('/photo'):
                    send_photo(take_photo())

        if GPIO.input(button_pin) == GPIO.HIGH and not runOnce:
            runOnce = True
            OnButtonDown()
        elif GPIO.input(button_pin) == GPIO.LOW and runOnce:
            runOnce = False
            GPIO.output(led_pin, GPIO.LOW) # led off

def OnButtonDown():
    for chat_id in ids:
        bot.send_chat_action(chat_id, 'upload_photo')    

    GPIO.output(led_pin, GPIO.HIGH)  # led on
    subprocess.call(["python3", "lcd.py", "proccessing..."])
    print("A picture is being taken...")

    file_name = take_photo()

    print("There is a guest waiting for your response!")
   
    send_photo(file_name, random.choice(guest_texts))

    subprocess.call(["python3", "lcd.py", "Waiting for\nresponse..."])

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
