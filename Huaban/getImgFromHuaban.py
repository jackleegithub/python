'''
从花瓣网（huaban.com）下载图片
缩略图页面：在JavaScript脚本中有一个变量存储着图片的信息的JSON数据,
    是一个数组，每个元素对应一个图片的详细信息，重要的信息有：
        pin_id, file.key, file.type
    其中file.key 就是图片的地址，使用了 url ReWrite技术
    app.page["pins"] = [
                        {
                            "pin_id": 321779677,
                            "user_id": 14112198,
                            "board_id": 16257864,
                            "file_id": 63664873,
                            "file": {
                                "id": 63664873,
                                "farm": "farm1",
                                "bucket": "hbimg",
                                "key": "86a6ad8dcfd27668815707d7fc6c70b34a2b50fd75027-vr01xE",
                                "type": "image/png",

                                .....
author:李志新
version:1.0.0
date:2017-12-27
'''
import requests
import urllib
import re
import json

#通过关键字和第几页，构建查询图片的url
def buildUrl(keyword, page):
    url = 'http://huaban.com/search/?'
    queryString = {
        'q':keyword,
        'category':'beauty',
        'jbobp33d':'',
        'page':page,
        'per_page':'20',
        'wfl':'1'
    }
    url = url + urllib.parse.urlencode(queryString)
    return url

def getImagesSrcType(url):#从缩略图页面上获取大图的地址和类型
    try:
        r = requests.get(url)
    except:
        return []
    p = re.compile(r'(?<=app.page\["pins"\] = ).+?(?=;\n)')
    data = re.findall(p, r.text)
    
    data = json.loads(data[0])
    imgSrcType = []
    for dt in data:
        srcType =[]
        srcType.append(dt['file']['key'])
        srcType.append(dt['file']['type'].split('/')[1])

        imgSrcType.append(srcType)
        
    return imgSrcType

def downloadImg(imgInfos, base = 'http://img.hb.aicdn.com/'):
    for info in imgInfos: #imgInfo是数组，每一个元素也是数组，一个是图片的URL，一个是图片类型
        url = base + info[0]
        try:
            r = requests.get(url)
        except:
            print("Get %s ERROR!" % url)
            
        filePath = "HuabanImages/" + info[0] + "." + info[1]
        with open(filePath, 'wb') as f:
            f.write(r.content)
            f.close()
            print("Dowlaod %s is finish!" % (url))

            
def main():
    keyword = input("Enter the key word for download image:")
    for i in range(1,2):
        print("\t\tDownlaod No. %d page" % i)
        url = buildUrl(keyword, i)
        downloadImg(getImagesSrcType(url))
        
    print("All images download FINISH!")


if __name__ == '__main__':
    main()
