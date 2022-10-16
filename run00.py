import RPi.GPIO as gpio
import time
import cv2
import numpy as np

pin1 = 35
pin2 = 36
pin3 = 37
pin4 = 38

gpio.setmode(gpio.BOARD)

gpio.setup(pin1, gpio.OUT)
gpio.setup(pin2, gpio.OUT)
gpio.setup(pin3, gpio.OUT)
gpio.setup(pin4, gpio.OUT)

center = 320
cap = cv2.VideoCapture(0)
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

  # 單看第400行的像素值
  color =BW[400] 
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
  direction = (center - 320)
  #畫出400行位置方便判斷
  cv2.line(BW, (0,400), (700,400), (0,0,0), 3)
  cv2.imwrite("BW.png",BW)
  #cv2.imshow('out',BW)
  #print(direction)                                #偏移量值

  # 停止
  if abs(direction) > 100:
       gpio.output(pin1, False)
       gpio.output(pin2, False)
       gpio.output(pin3, False)
       gpio.output(pin4, False)
  # 右轉
  elif direction >= 0:
       gpio.output(pin1, False)
       gpio.output(pin2, True)
       gpio.output(pin3, False)
       gpio.output(pin4, False)
  # 左转
  elif direction < 0:
       gpio.output(pin1, False)
       gpio.output(pin2, False)
       gpio.output(pin3, False)
       gpio.output(pin4, True)

  if cv2.waitKey(1) & 0xFF == ord('q'):
       gpio.output(pin1, False)
       gpio.output(pin2, False)
       gpio.output(pin3, False)
       gpio.output(pin4, False)
  elif white_count>stop:
       gpio.output(pin1, False)
       gpio.output(pin2, False)
       gpio.output(pin3, False)
       gpio.output(pin4, False)
       break

# 释放清理
cap.release()
cv2.destroyAllWindows()
pwm1.stop()
pwm2.stop()
pwm3.stop()
pwm4.stop()
gpio.cleanup()
