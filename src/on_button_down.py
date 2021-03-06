import RPi.GPIO as GPIO
import subprocess
from photo_ops import send_photo, take_photo
import consts
import random
import threading


def OnButtonDown(bot, ids):
    global long_thread

    GPIO.output(consts.led_pin, GPIO.HIGH)
    for chat_id in ids:
        bot.send_chat_action(chat_id, 'upload_photo')

    subprocess.call(["python3", "lcd.py", "Proccessing..."])
    print("A picture is being taken...")

    GPIO.output(consts.buzzer_pin, GPIO.HIGH)

    file_name = take_photo()
    send_photo(ids, bot, file_name, random.choice(consts.guest_texts))

    subprocess.call(["python3", "lcd.py", "Waiting for\nresponse..."])
    print("There is a guest waiting for your response!") 