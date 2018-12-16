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

audio_recording_process = None
audio_file_wav = consts.audio_dir + '/record.wav'
audio_file_mp3 = consts.audio_dir + '/record.mp3'
audio_recording_cmd = ('arecord -d 0 -c 2 -f S16_LE -r 44100 -t wav ' + audio_file_wav).split()
audio_wav_to_mp3_cmd = ('lame -h ' + audio_file_wav + ' ' + audio_file_mp3).split()

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)               # Numbers GPIOs by physical location
    GPIO.setup(consts.led_pin, GPIO.OUT)   # Set led_pin's mode is output
    GPIO.output(consts.led_pin, GPIO.HIGH) # Set led_pin high(+3.3V) to turn on led
    GPIO.setup(consts.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(consts.audio_btn_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(consts.buzzer_pin, GPIO.OUT)

def destroy():
    GPIO.output(consts.led_pin, GPIO.LOW)      # led off
    GPIO.cleanup()                             # Release resource
    print("\n\n* Program is terminated!")

def main():
    global audio_recording_process
    
    runOnce = True
    run_audio_btn_once = True

    while True:
        if GPIO.input(consts.button_pin) == GPIO.HIGH and not runOnce:
            runOnce = True
            GPIO.output(consts.buzzer_pin, GPIO.LOW)
            OnButtonDown(bot, ids)

        elif GPIO.input(consts.button_pin) == GPIO.LOW and runOnce:
            runOnce = False
            GPIO.output(consts.buzzer_pin, GPIO.HIGH)
            GPIO.output(consts.led_pin, GPIO.LOW)  # led off

        if GPIO.input(consts.audio_btn_btn) == GPIO.HIGH and not run_audio_btn_once:
            run_audio_btn_once = True

            if audio_recording_process is not None:
                audio_recording_process.kill()
            
            audio_recording_process = subprocess.Popen(audio_recording_cmd)

        elif GPIO.input(consts.audio_btn_btn) == GPIO.LOW and run_audio_btn_once:
            run_audio_btn_once = False
            if audio_recording_process is not None:
                audio_recording_process.kill()
                subprocess.call(audio_wav_to_mp3_cmd)

                for chat_id in ids:
                    bot.send_audio(chat_id, open(audio_file_mp3, 'rb'))

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
