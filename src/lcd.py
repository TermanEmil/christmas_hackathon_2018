"""Simple test for monochromatic character LCD on Raspberry Pi"""
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
from sys import argv

# Modify this if you have a different sized character LCD

def _lcd():
    lcd_columns = 16
    lcd_rows = 2

    lcd_rs = digitalio.DigitalInOut(board.D25)
    lcd_en = digitalio.DigitalInOut(board.D24)
    lcd_d7 = digitalio.DigitalInOut(board.D22)
    lcd_d6 = digitalio.DigitalInOut(board.D18)
    lcd_d5 = digitalio.DigitalInOut(board.D27)
    lcd_d4 = digitalio.DigitalInOut(board.D23)
    lcd_backlight = digitalio.DigitalInOut(board.D4)

    # Initialise the lcd class
    lcd = characterlcd.Character_LCD_Mono(
        lcd_rs,
        lcd_en,
        lcd_d4,
        lcd_d5,
        lcd_d6,
        lcd_d7,
        lcd_columns,
        lcd_rows,
        lcd_backlight
    )
    lcd.backlight = True

    return lcd
lcd = _lcd()

# print(argv[1])
lcd.message = argv[1]
