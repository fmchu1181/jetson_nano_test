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

width = 320  #定义摄像头获取图像宽度
height = 320   #定义摄像头获取图像长度

vp.set(cv2.CAP_PROP_FRAME_WIDTH, width)  #设置宽度
vp.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  #设置长度
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


        # 单看第470行的像素值
        color =BW[250]
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

        # 单看第350行的像素值
        color =BW[200]
        # 找到黑色的像素点个数
        white_count1 = np.sum(color == 0)
        # 找到黑色的像素点索引
        white_index1 = np.where(color == 0)
        # 防止white_count=0的报错
        if white_count1 ==0:
            white_count1= 1
        if np.size(white_count1) ==0:
            continue
        if np.size(white_index1)==0:
            continue
        # 找到白色像素的中心点位置
        center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
        center1 = (white_index1[0][white_count1 - 1] + white_index1[0][0]) / 2
        # 计算出center与标准中心点的偏移量（圖片預設像素為480*640）X軸為640

        x0=160-center
        x1=160-center1
        x3=x0-x1
        x=center-center1
        y=470-250
        direction=(y/x)
        cv2.line(BW, (int(center),250), (int(center1),200), (255, 255,255), 3)
        cv2.imwrite("BW.png",BW)
        cv2.imshow('out',BW)
        print(direction,x,center)                            #偏移量值
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
            break

        if abs(direction)>100:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(50)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(50)
        elif 100>direction>50:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(40)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(60)
        elif -100<direction<-50:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(60)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(40)

        elif 50>direction>20:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(30)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(70)
        elif -50<direction<-20:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(70)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(30)



    
# 释放清理
finally:
    vp.release()
    cv2.destroyAllWindows()
    gpio.cleanup()