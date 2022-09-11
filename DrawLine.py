import cv2
import numpy as np

vp= cv2.VideoCapture(0)

return_value, img= vp.read()
cv2.line(img, (0, 400), (650,400), (0, 0,0), 2)
cv2.imwrite("1.png", img)
cv2.imshow('out',img)
cv2.waitKey(0)

vp.release()
cv2.destroyAllWindows()