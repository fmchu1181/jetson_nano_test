#基於黑線偏移量值開始尋機
import RPi.GPIO as gpio
#import time
import cv2
import numpy as np

# 定义引脚
gpio.setmode(gpio.BOARD)
pin1 = 35
pin2 = 36
pin3 = 37
pin4 = 38

gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)
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
        ret,BW= cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY_INV) 
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
        if abs(direction) > 250:
                gpio.output(pin1, False)
                gpio.output(pin2, False)
                gpio.output(pin3, False)
                gpio.output(pin4, False)

        # 右转
        elif direction >= 0:
            # 限制在70以内
            if direction > 70:
                direction = 70
            gpio.output(pin1, False)
            gpio.output(pin2, True)
            gpio.output(pin3, False)
            gpio.output(pin4, False)

        # 左转
        elif direction < 0:
            if direction < -70:
                direction = -70
            gpio.output(pin1, False)
            gpio.output(pin2, False)
            gpio.output(pin3, False)
            gpio.output(pin4, True)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
# 释放清理
finally:
    vp.release()
    cv2.destroyAllWindows()
    gpio.cleanup()