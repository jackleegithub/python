'''
人脸注册：
人脸识别:

'''
import requests
import cv2
import base64


def getAK():
    ak = '24.ae4c1f1f8b9c2e9e88711b830060ae95.2592000.1524619428.282335-10846706'
    return ak
def registerByCapture():
    cap = cv2.VideoCapture(0)
    while True:
        r,frame = cap.read()
        cv2.imshow('Face', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:
            uid = input('Enter the user id:')
            cv2.imwrite('faceRegister.jpg', frame)
            with open('faceRegister.jpg','rb') as f:
                img = bytes.decode(base64.b64encode(f.read()))
            r = faceRegister(uid, img)
            if r:
                print('Register ok')
            else:
                print('Register ERROR.')
        elif key==ord('q'):
            break
        
    cap.release()
    cv2.destroyWindow('Face')

    
def faceRegister(uid, img, userInfo = ''):                
    ak = getAK()
    url = 'https://aip.baidubce.com/rest/2.0/face/v2/faceset/user/update?access_token=' + ak
    headers = {'Content-Type':'application/x-www-form-urlencoded'}
    params = {
        'uid':uid,
        'image':img,
        'user_info':userInfo,
        'group_id':'lzx',
        'action_type':'replace'
        }
    r = requests.post(url, headers = headers, data = params)
    if r.status_code == requests.codes.ok:
        if r.json().get('error_code') == None:
            return True
    return False

if __name__ == '__main__':
    registerByCapture()
