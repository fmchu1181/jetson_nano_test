import requests
import cv2
cp=cv2.VideoCapture(1)
return_value, img = cp.read(1)
cv2.imwrite("Picture1.png", img)
del(cp)
cv2.imshow('out1',img)

cv2.destroyAllWindows()
token = 'Ogx5oQamyLtobJTYWobK452VwdsTpZ2ifQkfptMcEgC'
message = 'test'
headers = { "Authorization": "Bearer " + token }
data = { 'message': message }
#files = {'imageFile': open(r'Picture1.png' , 'rb')}
files= {'imageFile': open('Picture1.png' , 'rb')}

requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data,files=files)