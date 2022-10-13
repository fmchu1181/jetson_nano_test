#拍照片
import cv2

# 設定從哪顆鏡頭讀取影像，在括弧中填入先前查詢到的webcam編號
webcam = cv2.VideoCapture(1)
cp=cv2.VideoCapture(0)
# 讀取影像
return_value, image = webcam.read(1)
return_value, img = cp.read(0)
# 儲存名為Picture.png的照片
cv2.imwrite("Picture.png", image)
cv2.imwrite("Picture1.jpg", img)
# 刪除webcam，避免影像佔用資源
del(webcam)
del(cp)
#show出剛剛拍的照片
cv2.imshow('out',image)
cv2.imshow('out1',img)
cv2.waitKey(0)

cv2.destroyAllWindows()