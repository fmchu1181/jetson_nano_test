from tkinter.ttk import LabelFrame
import RPi.GPIO as gpio
import time
import cv2
import numpy as np
import requests

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
cap=cv2.VideoCapture(1)

#linenotify 驗證碼
token = 'Ogx5oQamyLtobJTYWobK452VwdsTpZ2ifQkfptMcEgC'

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
        #cv2.imshow('out',BW)
        #print(direction)                                #偏移量值

        # 停止
        if abs(direction) > 100:
            gpio.output(pin1, False)
            pwm2.ChangeDutyCycle(30)
            gpio.output(pin3, False)
            pwm4.ChangeDutyCycle(30)

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

#右轉           t轉彎時間
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
        #cv2.imshow('out',BW)
        #print(direction)                                #偏移量值

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

#左轉           t轉彎時間
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
        #cv2.imshow('out',BW)
        #print(direction)                                #偏移量值

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

#無敵直走   L直走時間
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
        #cv2.imshow('out',BW)
        #print(direction)                                #偏移量值

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

#轉彎           t後退時間
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
        #cv2.imshow('out',BW)
        #print(direction)                                #偏移量值

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

#倒車           t後退時間
def baku(t):    
        turn(2)
        www(0.1)
        w()
        gpio.output(pin1, True)
        pwm2.ChangeDutyCycle(0)
        gpio.output(pin3, True)
        pwm4.ChangeDutyCycle(0)
        time.sleep(t)
        gpio.output(pin1, False)
        pwm2.ChangeDutyCycle(0)
        gpio.output(pin3, False)
        pwm4.ChangeDutyCycle(0)

message = 'test'
headers = { "Authorization": "Bearer " + token }
data = { 'message': message }
files= {'imageFile': open('Picture1.png' , 'rb')}

#拍照＋傳送
def pic():
    requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data,files=files)

while True:
    #0   ad 2.5      T 2
    stop=100

    ch = input("車子移動路徑 ： q結束程式 , z停止 , all走全程 , a第一房 , b第二房 , c第三房 , d第四房 , e第五房")
    if ch == 'all':
    #0   ad 2.5      T 2

        stop=100
        www(0.1)
        w()
        www(0.1)
        w()
        ##########
        ret ,imgg = cap.read(1)
        cv2.imwrite("A.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'A號房'
        data = { 'message': message }
        files= {'imageFile': open( 'A.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        del(imgg)
        cap.release()
        cap=cv2.VideoCapture(1)
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
        ret ,imgg= cap.read(1)
        cv2.imwrite("B.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'B號房'
        data = { 'message': message }
        files= {'imageFile': open( 'B.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        del(imgg)
        cap.release()
        cap=cv2.VideoCapture(1)
        ##########
        turn(2)
        www(0.1)
        w()
        www(0.1)
        w()
        ##########
        ret ,imgg = cap.read(1)
        cv2.imwrite("C.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'C號房'
        data = { 'message': message }
        files= {'imageFile': open( 'C.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        del(imgg)
        cap.release()
        cap=cv2.VideoCapture(1)
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
        ret, imgg = cap.read(1)
        cv2.imwrite("D.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'D號房'
        data = { 'message': message }
        files= {'imageFile': open( 'D.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        del(imgg)
        cap.release()
        cap=cv2.VideoCapture(1)
        ##########
        turn(1.9)
        www(0.1)
        w()
        www(0.1)
        w()
        ##########
        ret, imgg = cap.read(1)
        cv2.imwrite("E.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'E號房'
        data = { 'message': message }
        files= {'imageFile': open( 'E.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        del(imgg)
        cap.release()
        cap=cv2.VideoCapture(1)
        ##########
        turn(1.9)
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

        baku(1.2)
    
    if ch == 'z':
        gpio.output(pin1, False)
        pwm2.ChangeDutyCycle(0)
        gpio.output(pin3, False)
        pwm4.ChangeDutyCycle(0)
        
    if ch == 'a':
        print(' a第一房')
        www(0.1)
        w()
        www(0.1)
        w()
        ##########
        return_value, imgg = cap.read(1)
        cv2.imwrite("A.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'A號房'
        data = { 'message': message }
        files= {'imageFile': open( 'A.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        cap.release()
        cap=cv2.VideoCapture(1)
        ##########
        turn(2)
        www(0.1)
        w()
        www(0.1)
        w()
        baku(1.2)

    if ch == 'b':
        print('b第二房')
        www(0.1)
        w()
        d(2.5)
        www(0.1)
        w()
        d(2.5)
        www(0.1)
        w()
        ##########
        return_value, imgg = cap.read(1)
        cv2.imwrite("A.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'B號房'
        data = { 'message': message }
        files= {'imageFile': open( 'A.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        cap.release()
        cap=cv2.VideoCapture(1)
        ##########
        turn(2)
        www(0.1)
        w()
        a(2.5)
        www(0.1)
        w()
        a(2.5)
        www(0.1)
        w()
        baku(1.2)

    if ch == 'c':
        print('c第三房')
        www(0.1)
        w()
        d(2.5)
        www(0.1)
        w()
        a(2.5)
        www(0.1)
        w()
        ##########
        return_value, imgg = cap.read(1)
        cv2.imwrite("A.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'C號房'
        data = { 'message': message }
        files= {'imageFile': open( 'A.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        cap.release()
        cap=cv2.VideoCapture(1)
        ##########
        turn(2)
        www(0.1)
        w()
        d(2.5)
        www(0.1)
        w()
        a(2.5)
        www(0.1)
        w()
        baku(1.2)

    if ch == 'd':
        print('d第四房')
        www(0.1)
        w()
        d(2.5)
        www(0.1)
        w()
        www(0.1)
        w()
        d(2.5)
        www(0.1)
        w()
        ##########
        return_value, imgg = cap.read(1)
        cv2.imwrite("A.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'D號房'
        data = { 'message': message }
        files= {'imageFile': open( 'A.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        cap.release()
        cap=cv2.VideoCapture(1)
        ##########
        turn(2)
        www(0.1)
        w()
        a(2.5)
        www(0.1)
        w()
        www(0.1)
        w()
        a(2.5)
        www(0.1)
        w()
        baku(1.2)

    if ch == 'e':
        print('e第五房')
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
        ##########
        return_value, imgg = cap.read(1)
        cv2.imwrite("A.png", imgg)
        cv2.imshow('pic', imgg)
        cv2.waitKey(0)    # 按下任意鍵停止
        message = 'E號房'
        data = { 'message': message }
        files= {'imageFile': open( 'A.png' , 'rb')}
        while(1):
            ch = input("傳送異常照片？ n ： 不要傳送照片。 y ： 傳送照片")
            if ch=='n':
                break
            if ch=='y':
                pic()
                break
        cap.release()
        cap=cv2.VideoCapture(1)
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
        baku(1.2)

    if ch == 'q':
        gpio.output(pin1, False)
        pwm2.ChangeDutyCycle(0)
        gpio.output(pin3, False)
        pwm4.ChangeDutyCycle(0)
        break

vp.release()
cap.release()
cv2.destroyAllWindows()
gpio.cleanup()