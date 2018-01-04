'''
url='http://musicapi.qianqian.com/v1/restserver/ting?'
    queryString={
        'method':'baidu.ting.song.play',
        'format':'jsonp',
        'callback':'jQuery1720834946290780753_1514555000923',
        'songid':songId,
        '_':'1514555005976'
返回歌曲信息的JSON数据，内有
 "bitrate": {
        "show_link": "http://zhangmenshiting.qianqian.com/data2/music/42578037/42578037.mp3?xcode=a34696f829a66e143cbb1604e4436b22",
        "free": 1,
        "song_file_id": 42578037,
        "file_size": 2153723,
        "file_extension": "mp3",
        "file_duration": 269,
        "file_bitrate": 64,
        "file_link": "http://zhangmenshiting.qianqian.com/data2/music/42578037/42578037.mp3?xcode=a34696f829a66e143cbb1604e4436b22",
        "hash": "65615715c822ee41d4761f0ea23d9cbed0c39063"
    }

'''
import requests
import urllib
import json
import re

#从缩略图页面获取歌曲的id song_id
#在HTML代码中 data-songdata='{ "id": "10494258" }'
#             <a href="/song/10494258"
def getSongIds(songName):
    url ='http://music.baidu.com/search?'
    queryString = {
        'fr':'ps',
        'ie':'utf-8',
        'key':songName
    }
    url += urllib.parse.urlencode(queryString)
    try:
        r = requests.get(url)
    except:
        print("Get ERROR %s." % url)
        return []
    # <a href="/song/10494258"
    p = re.compile(r'(?<=href="/song/)\d+(?=" )')
    
    return re.findall(p, r.text)

#给定歌曲的song_id，获取歌曲的Mp3 地址列表和歌名
def getSongInfoBySongId(songId):
    url='http://musicapi.qianqian.com/v1/restserver/ting?'
    queryString={
        'method':'baidu.ting.song.play',
        'format':'jsonp',
        'callback':'jQuery1720834946290780753_1514555000923',
        'songid':songId,
        '_':'1514555005976'
    }

    url += urllib.parse.urlencode(queryString)
    
    try:
        r = requests.get(url)
    except:
        print("ERROR for get {}".format(url))
        return []
    
    beg = r.text.find('(')
    try:
        data = json.loads(r.text[beg + 1 : -2])
    except:
        print("ERROR on get information by song id of {}".format(songId))

    mp3Info = {}
    mp3Info['songId'] = songId
    mp3Info['title']=re.sub(r'[/\\()"]', '_', data['songinfo']['title'])#替换特殊字符
    mp3Info['author']=data['songinfo']['author']
    mp3Info['extension'] = '.' + data['bitrate']['file_extension']
    mp3Info['bitrate'] = data['bitrate']['file_bitrate']
    mp3Info['url']=data['bitrate']['file_link']

    return mp3Info

#通过url 下载Mp3 文件
def downloadMp3(mp3Info):
    
    try:
        r = requests.get(mp3Info['url'])        
    except:
        print("Downlaod ERROR in {}.".format(mp3Info['url']) )

    filePath = 'Mp3\\' + mp3Info['title'] + mp3Info['author'] + mp3Info['songId'] +  mp3Info['extension']
    with open(filePath, 'wb') as f:
        f.write(r.content)
        f.close()
    print("Downlaod {} Successful at {}.".format(mp3Info['title'], mp3Info['url']))
    
def main():
    songName = input("Enter the song name:")
    for id in getSongIds(songName):
        downloadMp3(getSongInfoBySongId(id))

    print("All song had download SUCCESSFUL!")

if __name__ == '__main__':
    main()

