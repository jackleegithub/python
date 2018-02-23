'''
人脸探测
'''

'''
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GgVkqMEPefeBB4X3ce2GuR11&client_secret=TgMfKcYrdpCGRB18AeWsGKUG2m5xPgzi'
access_token:"24.2201a0d41eab30a1abfadeb0a7b30066.2592000.1521961043.282335-10846706"
'''
import base64
import requests


url = "https://aip.baidubce.com/rest/2.0/face/v1/detect"

# 二进制方式打开图片文件
with open('face3.jpg', 'rb') as f:
    img = base64.b64encode(f.read())
f.close()

access_token="24.2201a0d41eab30a1abfadeb0a7b30066.2592000.1521961043.282335-10846706"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {"face_fields":"age,beauty,expression,faceshape,gender,glasses,landmark,race,qualities","image":img,"max_face_num":5}

url  += "?access_token=" + access_token
r = requests.post(url, data = payload, headers = headers)

if r.json():
    print("age:{}, beauty:{}".format(r.json()['result'][0]['age'], r.json()['result'][0]['beauty']))
