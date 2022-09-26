
#motor test
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

pin1 = 35
pin2 = 32
pin3 = 36
pin4 = 33

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
GPIO.setup(pin3, GPIO.OUT)
GPIO.setup(pin4, GPIO.OUT)
# 设置PWM波,频率为500Hz
pwm2 = GPIO.PWM(pin2, 500)
pwm4 = GPIO.PWM(pin4, 500)

# pwm波控制初始化
pwm2.start(0)
pwm4.start(0)

while True:
    ch = input("車子如何移動 w往前  s往後 a往左  d往右 q結束")
    if ch == 'q':
        GPIO.output(pin1, False)
        pwm2.ChangeDutyCycle(0)
        GPIO.output(pin3, False)
        pwm4.ChangeDutyCycle(0)
        break
    if ch == 'w':
        GPIO.output(pin1, False)
        pwm2.ChangeDutyCycle(30)
        GPIO.output(pin3, False)
        pwm4.ChangeDutyCycle(30)
    if ch == 's':
        GPIO.output(pin1, True)
        pwm2.ChangeDutyCycle(0)
        GPIO.output(pin3, True)
        pwm4.ChangeDutyCycle(0)
    if ch == 'd':
        GPIO.output(pin1, False)
        pwm2.ChangeDutyCycle(30)
        GPIO.output(pin3, False)
        pwm4.ChangeDutyCycle(0)
    if ch == 'a':
        GPIO.output(pin1, False)
        pwm2.ChangeDutyCycle(0)
        GPIO.output(pin3, False)
        pwm4.ChangeDutyCycle(30)
    if ch =='e':
        GPIO.output(pin1, False)
        pwm2.ChangeDutyCycle(0)
        GPIO.output(pin3, False)
        pwm4.ChangeDutyCycle(0)