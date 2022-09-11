import RPi.GPIO as gpio
import time


gpio.setwarnings(False)
# 设置GPIO口为BOARD编号规范
gpio.setmode(gpio.BOARD)
# 定义引脚
pin1 = 36
pin2 = 35
pin3=32
hz=500
# 设置GPIO口为输出
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)

# 设置PWM波,频率为500Hz
pwm3 = gpio.PWM(pin3, hz)

# pwm波控制初始化
pwm3.start(0)



pwm3.ChangeDutyCycle(100)
gpio.output(pin1, False)
gpio.output(pin2, True)
time.sleep(2)

pwm3.stop()


gpio.cleanup()