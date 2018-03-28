import requests
import base64
import cv2
import numpy

          
#画出72个点
def drawPoints(image, points,color = (0,255,0)):
    for pt in points:
        point = int(pt['x']),int(pt['y'])
        radius = 2
        cv2.circle(image, point, radius, color, -1)


#利用opencv中的polylines 画线，
#addStart，增加起始点
#addEnd，新增结束点
def drawLines(image,data, start, end, boolean = True, addStart = None, addEnd = None,color=(255,0,0)):
    arr = []
    for i in range(start, end):
        arr.append([data['landmark72'][i]['x'], data['landmark72'][i]['y']])
    if addStart:
        arr.insert(0, addStart)
    if addEnd:
        arr.append(addEnd)
        
    pts = numpy.array(arr,numpy.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(image, [pts], boolean, color)

def faceDetect(path):
    ak = '24.ae4c1f1f8b9c2e9e88711b830060ae95.2592000.1524619428.282335-10846706'
    url ='https://aip.baidubce.com/rest/2.0/face/v2/detect?access_token=' + ak
    with open(path, 'rb') as f:
        img = base64.b64encode(f.read())
    params = {"face_fields":"age,beauty,gender,landmark,landmark72","image":img,"max_face_num":10}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.post(url, headers = headers, data = params)

    frame = cv2.imread(path)

    for data in r.json()['result']:
        drawPoints(frame,data['landmark72'])
    
        drawLines(frame,data, 0, 13, False)#画脸
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
        cv2.putText(frame,"Age:{}.Sex:{}".format(data['age'], data['gender']),(x, y-10),font,0.6,(0,255,255), 1)
    cv2.imshow('Face',frame)    

    
    while True:
        if cv2.waitKey(0) == 32:
            break
    
    cv2.destroyWindow('Face')


if __name__ == '__main__':
    
    #global var
    imgPath = 'face.jpg'
    faceDetect(imgPath)
    
