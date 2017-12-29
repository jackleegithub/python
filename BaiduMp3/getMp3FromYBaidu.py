'''
从百度音乐人（http://y.baidu.com）下载音乐


'''
import urllib
import requests
import json
import re
import random

#从缩略图页面获取歌曲的id song_id
#在JavaScrip代码中 song sid-371201\" data-id=\"371201
#<script>MiniPipe.fragmentArrive({json}, window.location);</script>
def getSongIds(songName):
    url ='http://y.baidu.com/search?'
    queryString = {
        'key':songName
    }
    url += urllib.parse.urlencode(queryString)
    try:
        r = requests.get(url)
    except:
        print("Get ERROR %s." % url)
        return []
    # data-id=\"371201\">
    p = re.compile(r'(?<=data-id=\\")\d+(?=\\">)')
    
    return re.findall(p, r.text)

#给定歌曲的song_id，获取歌曲的Mp3 地址列表和歌名
def getSongInfoBySongId(songId):
    url ='http://y.baidu.com/app/song/infolist?'
    queryString={
        'callback':'jQuery1111015205029486288502_1514511255726',
        'song_id':songId,
        '_':'1514511255727'
    }
    url += urllib.parse.urlencode(queryString)
    print(url)
    try:
        r = requests.get(url)
    except:
        print("Get ERROR %s." % url)
        return []
    
    beg = r.text.find('(') + 1
    data = json.loads(r.text[beg:-1])
    mp3Info = {}
    if data['data'] and data['data'][0]:
        mp3Info['title'] = data['data'][0]['title']
        urls=[]
        for item in data['data'][0]['link_list']:
            urls.append(item['file_link'])
        mp3Info['urls'] = urls
        
    return mp3Info

#通过url 下载Mp3 文件
def downloadMp3(mp3Info):
    

    for url in mp3Info['urls']:
        try:
            r = requests.get(url)        
        except:
            print("Downlaod ERROR ." )
        
        p = re.compile(r'(?<=/)\d+\..+?(?=\?)')
        if re.findall(p, url):
            numberName = re.findall(p, url)[0]
        else:
            numberName = str(random.random()) + ".mp3"
        print("Downlaod {} at {}.".format(mp3Info['title'], url))
        
        filePath = 'Mp3\\' + mp3Info['title'] + numberName
        with open(filePath, 'wb') as f:
            f.write(r.content)
            f.close()

def main():
    songName = input("Enter the song name:")
    for id in getSongIds(songName):
        downloadMp3(getSongInfoBySongId(id))

if __name__ == '__main__':
    main()
