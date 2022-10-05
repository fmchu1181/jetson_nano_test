from tkinter.ttk import LabelFrame
import RPi.GPIO as gpio
import time
import cv2
import numpy as np

# 定義pin腳
gpio.setmode(gpio.BOARD)
pin1 = 35
pin2 = 32
pin3 = 36
pin4 = 33
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)

# 設置PWM波,频率为500Hz
pwm2 = gpio.PWM(pin2, 500)
pwm4 = gpio.PWM(pin4, 500)

# pwm波控制初始化
pwm2.start(0)
pwm4.start(0)

#設定攝影機
vp= cv2.VideoCapture(0)
#圖片預設大小為640*480

width = 320  #更改攝像頭預設寬度
height = 320   #更改攝像頭預設長度

vp.set(cv2.CAP_PROP_FRAME_WIDTH, width)  #設置寬度
vp.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  #設置長度

#徇跡停止判斷
stop=150

#前進
def w():
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
        ret, BW = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY) #白底黑線

        # 單看第280行的像素值
        color =BW[280] 
        # 找到黑色的像素點個數
        white_count = np.sum(color == 0)
        # 找到黑色的像素點位置
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

        # 計算出黑線與中心點偏移量值
        direction = (center - 160)*0.4      #0.4為比例值
        #畫出200行位置方便判斷
        cv2.line(BW, (0,275), (400,275), (0,0,0), 3)
        cv2.imwrite("BW.png",BW)
        cv2.imshow('out',BW)
        print(direction)                                #偏移量值

        # 停止
        if abs(direction) > 100:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)

        # 右轉
        elif direction >= 0:
            # 限制在50以内
            if direction > 50:
                direction = 50
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(40 + direction)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(30)

        # 左转
        elif direction < 0:
            if direction < -50:
                direction = -50
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(30)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(40 - direction)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
        elif white_count>stop:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
            break


#右轉
def d(t):
    gpio.output(pin1, False)
    pwm2.ChangeDutyCycle(0)
    gpio.output(pin3, False)
    pwm4.ChangeDutyCycle(0)
    time.sleep(0.2)
    gpio.output(pin1, False)
    pwm2.ChangeDutyCycle(60)
    gpio.output(pin3, False)
    pwm4.ChangeDutyCycle(0)
    time.sleep(t)
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
        ret, BW = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY) #白底黑線

        # 單看第200行的像素值
        color =BW[280] 
        # 找到黑色的像素點個數
        white_count = np.sum(color == 0)
        # 找到黑色的像素點位置
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

        # 計算出黑線與中心點偏移量值
        direction = (center - 160)*0.4      #0.4為比例值
        #畫出200行位置方便判斷
        cv2.line(BW, (0,275), (400,275), (0,0,0), 3)
        cv2.imwrite("BW.png",BW)
        cv2.imshow('out',BW)
        print(direction)                                #偏移量值

        if direction > 3:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(40)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
        

 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
        elif direction<3:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
            break


#左轉
def a(t):
    gpio.output(pin1, False)
    pwm2.ChangeDutyCycle(0)
    gpio.output(pin3, False)
    pwm4.ChangeDutyCycle(0)
    time.sleep(0.2)
    gpio.output(pin1, False)
    pwm2.ChangeDutyCycle(0)
    gpio.output(pin3, False)
    pwm4.ChangeDutyCycle(60)
    time.sleep(t)
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
        ret, BW = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY) #白底黑線

        # 單看第200行的像素值
        color =BW[280] 
        # 找到黑色的像素點個數
        white_count = np.sum(color == 0)
        # 找到黑色的像素點位置
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

        # 計算出黑線與中心點偏移量值
        direction = (center - 160)*0.4      #0.4為比例值
        #畫出200行位置方便判斷
        cv2.line(BW, (0,275), (400,275), (0,0,0), 3)
        cv2.imwrite("BW.png",BW)
        cv2.imshow('out',BW)
        print(direction)                                #偏移量值

        if direction < -3:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(40)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
        elif direction >-3:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
            break

#無敵直走
def www(L):
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
        ret, BW = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY) #白底黑線

        # 單看第200行的像素值
        color =BW[280] 
        # 找到黑色的像素點個數
        white_count = np.sum(color == 0)
        # 找到黑色的像素點位置
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

        # 計算出黑線與中心點偏移量值
        direction = (center - 160)*0.4      #0.4為比例值
        #畫出200行位置方便判斷
        cv2.line(BW, (0,275), (400,275), (0,0,0), 3)
        cv2.imwrite("BW.png",BW)
        cv2.imshow('out',BW)
        print(direction)                                #偏移量值

        gpio.output(pin1, False)
        pwm2.ChangeDutyCycle(40)
        gpio.output(pin3, False)
        pwm4.ChangeDutyCycle(40)
        time.sleep(L)
        gpio.output(pin1, False)
        pwm2.ChangeDutyCycle(0)
        gpio.output(pin3, False)
        pwm4.ChangeDutyCycle(0)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
            break
        elif white_count<100:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
            break


#轉彎
def turn(t):
    gpio.output(pin1, False)
    pwm2.ChangeDutyCycle(0)
    gpio.output(pin3, False)
    pwm4.ChangeDutyCycle(0)
    time.sleep(0.2)
    gpio.output(pin1, True)
    pwm2.ChangeDutyCycle(0)
    gpio.output(pin3, False)
    pwm4.ChangeDutyCycle(100)
    time.sleep(t)
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
        ret, BW = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY) #白底黑線

        # 單看第200行的像素值
        color =BW[280] 
        # 找到黑色的像素點個數
        white_count = np.sum(color == 0)
        # 找到黑色的像素點位置
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

        # 計算出黑線與中心點偏移量值
        direction = (center - 160)*0.4      #0.4為比例值
        #畫出200行位置方便判斷
        cv2.line(BW, (0,275), (400,275), (0,0,0), 3)
        cv2.imwrite("BW.png",BW)
        cv2.imshow('out',BW)
        print(direction)                                #偏移量值

        if direction > 3:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
    
 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
        elif direction<3:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(0)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(0)
            break

#0   ad 2.5      T 2

stop=100
w()
www(0.1)
w()
##########
turn(2)
www(0.1)
w()

a(2.5)
www(0.1)
w()
d(2.5)
www(0.1)
w()
##########
turn(2)
www(0.1)
w()
www(0.1)
w()
##########
turn(2)
www(0.1)
w()

a(2.5)
www(0.1)
w()
d(2.5)
www(0.1)
w()
##########
turn(2)
www(0.1)
w()
www(0.1)
w()
##########
turn(2)
www(0.1)
w()

d(2.5)
www(0.1)
w()
www(0.1)
w()
a(2.5)
www(0.1)
w()
turn(2)
www(0.1)
w()
gpio.output(pin1, True)
pwm2.ChangeDutyCycle(0)
gpio.output(pin3, True)
pwm4.ChangeDutyCycle(0)
time.sleep(1.2)
gpio.output(pin1, False)
pwm2.ChangeDutyCycle(0)
gpio.output(pin3, False)
pwm4.ChangeDutyCycle(0)

vp.release()
cv2.destroyAllWindows()
gpio.cleanup()