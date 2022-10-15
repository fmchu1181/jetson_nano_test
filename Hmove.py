#尋找黑線偏移量值
import cv2
import numpy as np
#call攝影機出來拍照
vp= cv2.VideoCapture(0)
return_value, img= vp.read()
cv2.imwrite("1.png", img)
#灰階
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 反二值化
ret,BW= cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY_INV) 
cv2.imwrite("BW.png",BW)
# 單看第400行的像素值
color =BW[400] 
# 找到黑色的像素點個數
white_count = np.sum(color == 0)
# 找到黑色的像素點位置
white_index = np.where(color == 0)
# 防止white_count=0的報錯
if white_count == 0:
    white_count = 1
# 找到白色像素的中心點位置
center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
#計算center與中心點偏移量值（640*480）
direction = center - 320
print(direction)                            #偏移量值
print(white_count)                     #黑點個數
print(white_index )                    #BW.png第400行黑色位置
#print(white_index [0][0])      #400行第一點黑點位置
#print(white_count - 1)            #在第400行第幾位為最後一位
print(center)                                  #中心點位置
print(white_index[0][white_count - 1])      #400行最後一點黑點位置