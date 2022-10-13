import requests

url = 'https://notify-api.line.me/api/notify'
token = 'Ogx5oQamyLtobJTYWobK452VwdsTpZ2ifQkfptMcEgC'
headers = {
    'Authorization': 'Bearer ' + token
}
data = {
    'message':'iiiiii',
    'imageThumbnail':'https://steam.oxxostudio.tw/downlaod/python/line-notify-demo.png',
    'imageFullsize':'https://steam.oxxostudio.tw/downlaod/python/line-notify-demo.png'
}
data = requests.post(url, headers=headers, data=data)