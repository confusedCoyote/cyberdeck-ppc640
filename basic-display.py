################################################################################

import board
import digitalio
import adafruit_ssd1306
import random
import string
import psutil
import cpuinfo
import socket
import fcntl
import struct
import collections
import smbus
import time
import subprocess
import os

################################################################################

from RPLCD import *
from time import sleep
from RPLCD.i2c import CharLCD
from datetime import datetime
from gpiozero import CPUTemperature, LoadAverage
from PIL import Image, ImageDraw, ImageFont

################################################################################

DEBUG = True

# Check to see if we are already running this script
processname = os.path.basename(__file__)
# Bit of an annoying exec command to see if it is already running - have to remove
# the grep from ps as this will give a false positive!
process_command_for_check = " ps -Af |grep 'python.*" + processname + "' |grep -v 'grep'"
tmp = os.popen(process_command_for_check).read()

if DEBUG:
	print(tmp)

# How many are running?
proccount = tmp.count(processname)
if proccount > 1:
	# Too many :( So we just bail here
	print(proccount, 'processes found for [', processname, ']')
	print("  Exiting")
	exit()
else:
	# We am winning so just continue.
	if DEBUG:
		print('[', processname, ']' + ' Not Running.')
		print("  Starting script")

# Include external "library files"
include_files = ["icons.py", "oledlib.py", "lcdlibs.py"]

if DEBUG:
	print("Checking [" + os.getcwd() + '/]')

for file in include_files:
	file_name = os.getcwd() + '/' + file
	exec(open(file_name).read())
	if DEBUG :
		print("[" + file + "] included")

## OLED physical sizes
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Text to center on a 2x16 LCD on top row[0]
#            0123456789012345
MAIN_TEXT = "CyberDeck PPC640"
ALT_TEXT =  "coyotepr.uk"

if DEBUG:
	print("Main Text : " + MAIN_TEXT)
	print(" Alt Text : " + ALT_TEXT)
'''

$ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- 23 -- -- -- 27 -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- 38 -- -- -- 3c -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --

0x23 - 2x16 LCD
0x27 - 4x20 LCD
0x38 - Temp / Humidity sensor
0x3c - 128x64 OLED

'''

i2c = board.I2C()
bus = smbus.SMBus(1)
lcd = CharLCD('PCF8574', 0x27)  # 20x4
lcd2 = CharLCD('PCF8574', 0x23) # 16x2
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

################################################################################
##   MAIN LOOP
################################################################################

wake_the_screens()

generate_special_chars()
the_ascii_printables = printable_ascii_chars();
who_am_i(MAIN_TEXT, lcd2, 16)

i = 0;
while True:
	if  i % 15 == 0 and i > 0:
		# When the "screen saver" kicks in...
		clear_lcd_line(0, 16, lcd2)
		who_am_i(ALT_TEXT, lcd2, 16)
		do_matrix_thing(the_ascii_printables)
		clear_lcd_line(0, 16, lcd2)

	who_am_i(MAIN_TEXT, lcd2, 16)

	oled.text(get_the_current_time("date"), 10, 0, 1)
	display_string_to_oled(2, 23, 0, 14, get_the_current_time("time", 0))
	oled.text(get_the_current_time("uptime"), 5, 50, 1)
	oled.show()

	System_information()

	i += 1
	sleep(1)

	display_string_to_oled(2, 23, 0, 14, get_the_current_time("time", 0))
	oled.text(get_the_current_time("uptime"), 5, 50, 1)
	oled.show()
	sleep(1)
	i += 1
	oled.fill(0)  # Clear the display

