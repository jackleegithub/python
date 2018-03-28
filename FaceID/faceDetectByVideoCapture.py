'''
使用 opencv-python 从摄像头获取 图像
使用 reqests 从ai.baidu.com 获取人脸信息
使用 opencv-python 画出信息点
'''
import cv2
import numpy
import requests
import base64

#画出72个点 
def drawPoints(image, data,  color = (0, 255,255), lineWidth = 1):
    for pt in data['landmark72']:
        coordinate = pt['x'], pt['y']
        radius = 2
        cv2.circle(image, coordinate, radius, color, lineWidth)

    return True

#画出从点start 到点 end 的线段，
#close，是否闭合
def drawLines(image, data, start, end,close = True, addStart = None, addEnd = None, color=(255,0,0),lineWidth=1):
    arrPoints = []
    for i in range(start, end):
        arrPoints.append([data['landmark72'][i]['x'], data['landmark72'][i]['y']])

    if addStart:
        arrPoints.insert(0, addStart)
    if addEnd:
        arrPoints.append(addEnd)
        
    arrPoints = numpy.array(arrPoints, numpy.int32)
    arrPoints = arrPoints.reshape((-1, 1, 2))
    cv2.polylines(image, [arrPoints], close, color, lineWidth)

def faceDetect():
    cap = cv2.VideoCapture(0)
    while True:
        r, frame = cap.read()
        cv2.imwrite('face.jpg', frame)
        
        with open('face.jpg','rb') as f:
            img = base64.b64encode(f.read())

        ak = '24.ae4c1f1f8b9c2e9e88711b830060ae95.2592000.1524619428.282335-10846706'
        url = 'https://aip.baidubce.com/rest/2.0/face/v1/detect?access_token=' + ak
        params = {"face_fields":"age,beauty,faceshape,gender,landmark,landmark72","image":img,"max_face_num":10}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        r = requests.post(url, headers = headers, data = params)

        for data in r.json()['result']:
            drawPoints(frame, data)

            drawLines(frame, data, 0, 13, False)#draw face
            drawLines(frame,data, 13, 21)#右眼
            drawLines(frame,data, 22, 30)#右眉毛
            drawLines(frame,data, 30, 38)#左眼
            drawLines(frame,data, 39, 47)#右眉毛
            drawLines(frame,data, 47, 57)#鼻子
            arr = []
            arr.append([data['landmark72'][51]['x'], data['landmark72'][51]['y']])
            arr.append([data['landmark72'][52]['x'], data['landmark72'][52]['y']])
            arr.append([data['landmark72'][57]['x'], data['landmark72'][57]['y']]) 
            pts = numpy.array(arr,numpy.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (255,0,0))
        
            drawLines(frame,data, 58, 66)#嘴
            drawLines(frame,data, 66, 69, False,[data['landmark72'][58]['x'], data['landmark72'][58]['y']],[data['landmark72'][62]['x'], data['landmark72'][62]['y']])#嘴
            drawLines(frame,data, 69, 72, False,[data['landmark72'][62]['x'], data['landmark72'][62]['y']],[data['landmark72'][58]['x'], data['landmark72'][58]['y']])#嘴
        
        
            x = data['location']['left']
            y = data['location']['top']
            w = data['location']['width']
            h = data['location']['height']
        
            #cv2.rectangle(image,Postition1, Position2, Color, Line-Width)
            #cv2.rectangle(frame,(x,y),(x+w, y + h),(0,0,255), 1)
        
            #cv2.putText(image, Text, Position, Font, Font-size, Color, Line-width)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,"Age:{:.0f}.Sex:{}".format(data['age'], data['gender']),(x, y-10),font,0.6,(0,255,255), 1)
        
        cv2.imshow('Face', frame)
        
        if cv2.waitKey(100) & 0xFF == 32:
                break
    cap.release()
    cv2.destroyWindow('Face')

if __name__ == '__main__':
    faceDetect()

