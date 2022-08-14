#二值化
import cv2

cap=cv2.VideoCapture(0)
return_value, img=cap.read()
cv2.imwrite("1.png", img)
img1= cv2.imread('1.png')
#二值化前先將圖片轉為灰階
img_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# 如果大於 127 就等於 0，反之等於 255
ret,BW= cv2.threshold(img_gray, 180, 255, cv2.THRESH_BINARY_INV) 

cv2.imwrite("BW.png", BW)
cv2.imshow('out', BW)
cv2.waitKey(0)    # 按下任意鍵停止
cv2.destroyAllWindows()
del(cap)