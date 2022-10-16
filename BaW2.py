import cv2
#讀取網路攝影機，讀取拍到照片用變數img命名，再存為2.png
cap=cv2.VideoCapture(0)

return_value, img=cap.read()
cv2.imwrite("2.png", img)
#讀取2.png轉為灰階圖再進行二值化
img = cv2.imread('2.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); # 轉換前，都先將圖片轉換成灰階色彩
ret, output1 = cv2.threshold(img_gray, 90, 255, cv2.THRESH_BINARY)     # 如果大於 127 就等於 255，反之等於 0。
ret, output2 = cv2.threshold(img_gray, 20, 255, cv2.THRESH_BINARY_INV) # 如果大於 127 就等於 0，反之等於 255。
ret, output3 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_TRUNC)      # 如果大於 127 就等於 127，反之數值不變。
ret, output4 = cv2.threshold(img_gray, 10, 255, cv2.THRESH_TOZERO)     # 如果大於 127 數值不變，反之數值等於 0。
ret, output5 = cv2.threshold(img_gray, 127, 255, cv2.THRESH_TOZERO_INV) # 如果大於 127 等於 0，反之數值不變。

#cv2.imshow('0', img)
cv2.imshow('1', output1)
#cv2.imshow('2', output2)
#cv2.imshow('3', output3)
#cv2.imshow('4', output4)
#cv2.imshow('5', output5)
cv2.imwrite("0.png", output1)
cv2.waitKey(0)    # 按下任意鍵停止
cv2.destroyAllWindows()
