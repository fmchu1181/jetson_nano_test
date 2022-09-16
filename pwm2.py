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
pwm1 = gpio.PWM(pin1, 50)
pwm2 = gpio.PWM(pin2, 50)


# pwm波控制初始化
pwm1.start(25)
pwm2.start(25)

pwm1.ChangeDutyCycle(0)
pwm2.ChangeDutyCycle(100)

time.sleep(2)

pwm1.stop()
pwm2.stop()

gpio.cleanup()