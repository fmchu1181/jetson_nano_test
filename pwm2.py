import RPi.GPIO as gpio
import time

pin1 = 32
pin2 = 33


# 设置GPIO口为BOARD编号规范
gpio.setmode(gpio.BOARD)

# 设置GPIO口为输出
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)


# 设置PWM波,频率为500Hz
pwm1 = gpio.PWM(pin1, 500)
pwm2 = gpio.PWM(pin2, 500)


# pwm波控制初始化
pwm1.start(0)
pwm2.start(0)

pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(20)
time.sleep(2)

pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(40)
time.sleep(2)

pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(60)
time.sleep(2)

pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(80)
time.sleep(2)
pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(100)
time.sleep(2)
pwm1.stop()
pwm2.stop()

gpio.cleanup()