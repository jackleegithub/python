'''
    生成百度热力图需要的经纬度的json格式数据
    数据来源是2015年中国主要城市GDP

    获取城市的经纬度的api：
    http://api.map.baidu.com/geocoder/v2/?address=白石头&output=json&ak=hwL60GxvLIDUGbAyDElHCq9p9i0Z4TN3

    参考 https://www.jianshu.com/p/773ff5f08a2c

    author：李志新
    date：2018-1-4
'''
import requests
import urllib

def getlnglat(city):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    ak = 'hwL60GxvLIDUGbAyDElHCq9p9i0Z4TN3'
    add = urllib.parse.urlencode({city:""})[:-1]
    url += "?address=" + add + "&output=json&ak=" + ak
   
    try:
        r = requests.get(url)
    except:
        print("Get web ERROR at {}".format(url))
        return None

    return r.json()

def getJOSN(inFile, outFile):
    outf = open(outFile, 'wt')
    with open(inFile, 'r') as inf:
        for line in inf.readlines()[1:]:
            arrLine = line.split(",")
            city = arrLine[1].strip()
            money= float(arrLine[2].strip())

            lnglat = getlnglat(city)
            
            if lnglat:
                if int(lnglat["status"]) > 0:
                    print("{}-Get {} information ERROR for {}".format(arrLine[0], city,lnglat["msg"]))
                else:
                    print("{}-Get {} information for longitude and latitude.".format(arrLine[0], city))
                    longitude = float(lnglat['result']['location']['lng'])
                    latitude = float(lnglat['result']['location']['lat'])
                    txt = '{"lng":%f,"lat":%f,"count":%f},\n' % (longitude, latitude, money)
                    outf.write(txt)
            else:
                print("{}-Get {} information ERROR for longitude and latitude.{}".format(arrLine[0], city,lnglat))
        inf.close()
    outf.close()
    
getJOSN("2015GDP.csv",'out.txt')
