#基於黑線偏移量值開始尋機
import RPi.GPIO as gpio
import time
import cv2
import numpy as np

# 定义引脚
gpio.setmode(gpio.BOARD)
pin1 = 35
pin2 = 32
pin3 = 36
pin4 = 33

gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)

# 设置PWM波,频率为500Hz
pwm2 = gpio.PWM(pin2, 500)
pwm4 = gpio.PWM(pin4, 500)

# pwm波控制初始化
pwm2.start(0)
pwm4.start(0)

vp= cv2.VideoCapture(0)
center=320
try:
    while(1):
        #call攝影機出來拍照
        return_value, img= vp.read()
        if return_value==False:
            continue
        cv2.imwrite("1.png", img)
        
        #灰階
        #cv2.imread("1.png",img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 反二值化
        #ret,BW= cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV) #黑底白線
        ret, BW = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY) #白底黑線
        cv2.imwrite("BW.png",BW)
        cv2.imshow('out',BW)
        # 单看第400行的像素值
        color =BW[400]
        # 找到黑色的像素点个数
        white_count = np.sum(color == 0)
        # 找到黑色的像素点索引
        white_index = np.where(color == 0)

        # 防止white_count=0的报错
        if white_count ==0:
            white_count = 1
        if np.size(white_count) ==0:
            continue
        if np.size(white_index )==0:
            continue
        # 找到白色像素的中心点位置
        center = (white_index[0][white_count - 1] + white_index[0][0]) / 2

        # 计算出center与标准中心点的偏移量（圖片預設像素為480*640）X軸為640
        direction = center - 320
        print(direction)                            #偏移量值

        # 停止
        if abs(direction) > 300:
                gpio.output(pin1, False)
                pwm2.ChangeDutyCycle(0)
                gpio.output(pin3, False)
                pwm4.ChangeDutyCycle(70)

        # 小右轉
        elif  direction >0:
            # 限制在70以内
            if direction >40:
                direction = 40
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(50 + direction)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)

        # 小左轉
        elif  direction <0:
            # 限制在70以内
            if direction <-40:
                direction = -40
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0 )
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(50- direction)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
            break
    
# 释放清理
finally:
    vp.release()
    cv2.destroyAllWindows()
    gpio.cleanup()