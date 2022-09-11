#motor test
import Jetson.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

pin1=35
pin2=36
pin3=37
pin4=38
t=0.05
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)

while True:
    ch = input("車子如何移動 w往前  s往後 a往左  d往右 q結束")
    if ch == 'q':
       GPIO.output(pin1, False)
       GPIO.output(pin2, False)
       GPIO.output(pin3, False)
       GPIO.output(pin4, False)
       break
    if ch == 'p':
       GPIO.output(pin1, False)
       GPIO.output(pin2, True)
       GPIO.output(pin3, False)
       GPIO.output(pin4, True)

    if ch == 'w':
       GPIO.output(pin1, False)
       GPIO.output(pin2, True)
       GPIO.output(pin3, False)
       GPIO.output(pin4, True)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, False)
       GPIO.output(pin3, False)
       GPIO.output(pin4, False)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, True)
       GPIO.output(pin3, False)
       GPIO.output(pin4, True)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, False)
       GPIO.output(pin3, False)
       GPIO.output(pin4, False)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, True)
       GPIO.output(pin3, False)
       GPIO.output(pin4, True)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, False)
       GPIO.output(pin3, False)
       GPIO.output(pin4, False)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, True)
       GPIO.output(pin3, False)
       GPIO.output(pin4, True)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, False)
       GPIO.output(pin3, False)
       GPIO.output(pin4, False)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, True)
       GPIO.output(pin3, False)
       GPIO.output(pin4, True)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, False)
       GPIO.output(pin3, False)
       GPIO.output(pin4, False)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, True)
       GPIO.output(pin3, False)
       GPIO.output(pin4, True)
       time.sleep(t)
       GPIO.output(pin1, False)
       GPIO.output(pin2, False)
       GPIO.output(pin3, False)
       GPIO.output(pin4, False)
       time.sleep(t)

    if ch == 's':
       GPIO.output(pin1, True)
       GPIO.output(pin2, False)
       GPIO.output(pin3, True)
       GPIO.output(pin4, False)
    if ch == 'd':
       GPIO.output(pin1, False)
       GPIO.output(pin2, True)
       GPIO.output(pin3, False)
       GPIO.output(pin4, False)
    if ch == 'a':
       GPIO.output(pin1, False)
       GPIO.output(pin2, False)
       GPIO.output(pin3, False)
       GPIO.output(pin4, True)