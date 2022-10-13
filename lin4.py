import requests
import cv2
cp=cv2.VideoCapture(1)
return_value, img = cp.read(1)
cv2.imwrite("Picture1.png", img)
cv2.imshow('out1',img)

token = 'Ogx5oQamyLtobJTYWobK452VwdsTpZ2ifQkfptMcEgC'
message = 'test'
message1='none'
headers = { "Authorization": "Bearer " + token }
data = { 'message': message }
data1 = { 'message': message1 }
#files = {'imageFile': open(r'Picture1.png' , 'rb')}
files= {'imageFile': open('Picture1.png' , 'rb')}
files1={'imageFile': open('0.png' , 'rb')}
while True:
    ch = input("車子如何移動 w往前  s往後 a往左  d往右 q結束")
    if ch == 'q':

       break
    if ch == 'w':
        requests.post("https://notify-api.line.me/api/notify",headers = headers, data = data,files=files)
    if ch =='e':
        pass
print('www')
cv2.destroyAllWindows()