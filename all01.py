import RPi.GPIO as gpio
import time
import cv2
import numpy as np

# 定義pin腳
gpio.setmode(gpio.BOARD)
pin1 = 35
pin2 = 36
pin3 = 37
pin4 = 38
gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)
#設定攝影機
vp= cv2.VideoCapture(0)
#圖片預設大小為640*480
center=320
#尋機停止判斷
stop=200
#轉彎時間
t=1
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
        
        #停止
        if abs(direction) > 250:
                gpio.output(pin1, False)
                gpio.output(pin2, False)
                gpio.output(pin3, False)
                gpio.output(pin4, False)

        #直走
        elif  -11<direction<11:
            gpio.output(pin1, False)
            gpio.output(pin2, True)
            gpio.output(pin3, False)
            gpio.output(pin4, True)
        # 右转
        elif direction >12:
            # 限制在70以内
            gpio.output(pin1, False)
            gpio.output(pin2, True)
            gpio.output(pin3, False)
            gpio.output(pin4, False)

        # 左转
        elif direction <  -12:
            gpio.output(pin1, False)
            gpio.output(pin2, False)
            gpio.output(pin3, False)
            gpio.output(pin4, True)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            gpio.output(pin1, False)
            gpio.output(pin2, False)
            gpio.output(pin3, False)
            gpio.output(pin4, False)
            break
        elif white_count > stop:
            gpio.output(pin1, False)
            gpio.output(pin2, False)
            gpio.output(pin3, False)
            gpio.output(pin4, False)
            break
#右轉
def d():
    gpio.output(pin1, False)
    gpio.output(pin2, False)
    gpio.output(pin3, False)
    gpio.output(pin4, False)
    time.sleep(0.1)
    gpio.output(pin1, False)
    gpio.output(pin2, True)
    gpio.output(pin3, False)
    gpio.output(pin4, False)
    time.sleep(t)            
    gpio.output(pin1, False)
    gpio.output(pin2, False)
    gpio.output(pin3, False)
    gpio.output(pin4, False)
def o():
    print('1')
w()
o()
d()

vp.release()
cv2.destroyAllWindows()
gpio.cleanup()