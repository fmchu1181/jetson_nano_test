import RPi.GPIO as gpio
import time
import cv2
import numpy as np
gpio.setmode(gpio.BOARD)
pin1 = 35
pin2 = 36
pin3 = 37
pin4 = 38
t=3
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)

gpio.output(pin1, False)
gpio.output(pin2, True)
gpio.output(pin3, False)
gpio.output(pin4, False)
time.sleep(t)          

cv2.destroyAllWindows()
gpio.cleanup()  