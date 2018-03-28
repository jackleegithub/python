'''
语音识别
'''

import requests
import base64


def getAK():
   
    url ='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=YGPvAHYLvqNSXOPtCOhVcTfG&client_secret=MA9z3RTOqVgGFEG0XZZrN3qglNrXep37'
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    r = requests.get(url, headers = headers)
    return r.json()['access_token']

ak = getAK()  #'24.ae4c1f1f8b9c2e9e88711b830060ae95.2592000.1524619428.282335-10846706'
url ='http://vop.baidu.com/server_api'
#headers = {'Content-Type':'application/x-www-form-urlencoded'}
headers = {'Content-Type':'application/json'}
with open('a.wav','rb') as f:
    wav = base64.b64encode(f.read())

params = {
    'format':'wav',
    'rate':16000,
    'channel':1,
    'cuid':'0A-00-27-00-00-0F',
    'token':ak,
    'speech':wav,
    'len':len(wav)
    }
r = requests.post(url, headers = headers, data = params)

if r.status_code == requests.codes.ok:
    print(r.text)

