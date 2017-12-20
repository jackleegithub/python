#从新浪图片中抓取图片
#列表页地址：http://search.sina.com.cn/?q=%E8%B7%91%E6%AD%A5&from=photo&c=img&slide=1&size=l&ie=utf-8       
#详细页地址，可以从上面网页中获取
#version:1.2
#date: 2017-12-20
#author:李志新
#
#不使用正则表达式(re模块)，使用JSON、BeautifulSoup 和字符串的切片等相关操作代替
import requests
import urllib # use urllib.parse.urlencode()方法，将字典（对象）序列化成url格式
from bs4 import BeautifulSoup
import json
import time #文件名
import hashlib

#删除url中斜杠\
def replaceSlash(urls):
   for i in range(len(urls)):
    urls[i] = urls[i].replace('\\', '')

def saveImageByUrl(url):
   r = requests.get(url)
   filePath = 'sinaImages/' + hashlib.md5(str(time.time()).encode(encoding='utf-8')).hexdigest() + '.jpg'
   with open(filePath, 'wb') as f:
      f.write(r.content)
      
def saveImageByUrls(urls):
   for url in urls:
      saveImageByUrl(url)


keyWord = input("Enter the search key world:")
#构建url，获取网页数据
url = 'http://search.sina.com.cn/?'
queryString = {
   'q':keyWord,
   'from':'photo',
   'c':'img',
   'slide':'1',
   'size':'l',
   'ie':'utf-8'
}
url = url + urllib.parse.urlencode(queryString)
headers = {
   'Cookie':'SINAGLOBAL=124.207.179.82_1444786879.413910; SGUID=1444787841917_79527098; vjuids=-27347c3c.15064111868.0.ad3519ad; U_TRS1=00000052.50432df.561dc0b1.5c9cfd80; SCF=AtnJG5mM9wxdYvjDngdW7CNj2Orr0_AuHEoDR3IsLMFcdOQmlJcZN_ZGrROFkyp81gq5gWPdAIlEGCeI82lWYrA.; UOR=,,; sso_info=v02m6alo5qztZ-apoWjmrW9rJmWlZ-Jp5WpmYO0tY2jhLOMo4y3jJOktQ==; SUB=_2AkMusgbVf8NxqwJRmPoTzWPmaohyyAnEieKY7vcOJRMyHRl-yD83qlETtRDB0J0UyHyxS7OHGtWv1SbL-DpW-Q..; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9W5KuXMubZ6BEy8.N07YQGQB; lxlrtst=1513048092_o; ArtiFSize=14; vjlast=1513067936.1513241128.10; lxlrttp=1513341002; Apache=58.129.155.129_1513728372.606110; ULV=1513728559955:615:27:7:58.129.155.129_1513728372.606110:1513643628983; rotatecount=3; U_TRS2=00000081.50a8148b.5a39aba6.d087bbca; WEB2_OTHER=d92c8cf420aac5a1c9ecf820f7839904',
   'Host':'search.sina.com.cn',
   'Upgrade-Insecure-Requests':'1',
   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

}
r = requests.get(url, headers = headers)

#构建BeautifulSoup，找出详细页的url，放在列表lsAHref中
soup = BeautifulSoup(r.content, 'html.parser',from_encoding="iso-8859-1")
lsAHref = []
lsDiv = soup.find_all('div', class_='cell')
for div in lsDiv:
   lsAHref.append(div.find('a')['href'])

#每一个详细页中获取详细图片，保存在文档当前目录中的sinaImage文件夹中。
#每张图片的信息保存在一个json字符串中，json字符串放在JavaScrip中的slide_data 变量里。
for url in lsAHref:
   print("Getting image from: %s" % url)
   r = requests.get(url)
   #r.encoding='gb2312'
   ##V1.2正则表达式
   #p = re.compile(r'(?<="image_url":").*?(?=",)')
   #lsImgSrc = re.findall(p, r.text)
   soup = BeautifulSoup(r.text, 'html.parser')
   div = soup.find('div', id="SI_Nav") #图片信息存放在Script中，div是它的前一个元素
   script = div.find_previous_sibling("script") #获取 script 元素，里面有图片url 的信息。
   txt = script.string.split("\n")[1] #获取存放图片信息JSON 的JavaScript 变量字符串
   pos = txt.find("{")

   dt = json.loads(txt[pos::]) #通过切片获取JSON 字符串
   
   lsImgSrc = []
   for img in dt['images']:
      lsImgSrc.append(img['image_url'])

   saveImageByUrls(lsImgSrc)
   
   



