import requests
import cv2
cp=cv2.VideoCapture(0)
return_value, img = cp.read(0)
cv2.imwrite("Picture1.png", img)
del(cp)
cv2.imshow('out1',img)

cv2.destroyAllWindows()
url = 'https://notify-api.line.me/api/notify'
token = 'Ogx5oQamyLtobJTYWobK452VwdsTpZ2ifQkfptMcEgC'
headers = {
    'Authorization': 'Bearer ' + token
}
data = {
    'message':'iiifvfrrriii',
    'imageThumbnail': 'http://csscoke.com/wp-content/uploads/2015/07/special_album_done_small.jpg',
    'imageFullsize':'http://csscoke.com/wp-content/uploads/2015/07/special_album_done_small.jpg'
}
data = requests.post(url, headers=headers, data=data)