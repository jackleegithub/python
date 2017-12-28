'''
从百度图片下载图片
百度图片在搜索的第一屏上，图片的地址是 objURL,图片的base64编码也在。
第n屏（n>=2)是通过XHR 动态加载，返回json数据，objURL是加密字符串
    秘钥是一个字符的对应关系，有2种映射：
    （1）多个字符映射为一个字符，'_z2C$q'=>':','_z&e3B'=>'.','AzdH3F'=>'/'。
    （2）单个字符映射为单字符。
'''
import urllib
import requests

def buildUrlForFirstPage(keyword):
    url = 'https://image.baidu.com/search/index?'

    queryString = {
        'tn':'baiduimage',
        'ipn':'r',
        'ct':'201326592',
        'cl':'2',
        'lm':'-1',
        'st':'-1',
        'fm':'index',
        'fr':'',
        'hs':'0',
        'xthttps':'111111',
        'sf':'1',
        'fmq':'',
        'pv':'',
        'ic':'0',
        'nc':'1',
        'z':'',
        'se':'1',
        'showtab':'0',
        'fb':'0',
        'width':'',
        'height':'',
        'face':'0',
        'istype':'2',
        'ie':'utf-8',
        'word':keyword,
        'oq':keyword,
        'rsp':'-1',
        }
    url = url + urllib.parse.urlencode(queryString)
    return url

# gsm = hex(pn)
def buildUrlForOtherPage(keyword, pn):
    url = 'https://image.baidu.com/search/acjson?'
    queryString = {
        'tn':'resultjson_com',
        'ipn':'rj',
        'ct':'201326592',
        'is':'',
        'fp':'result',
        'queryWord':keyword,
        'cl':'2',
        'lm':'-1',
        'ie':'utf-8',
        'oe':'utf-8',
        'adpicid':'',
        'st':'-1',
        'z':'9',#图片尺寸 3大尺寸， 9特大尺寸
        'ic':'0',
        'word':keyword,
        's':'',
        'se':'',
        'tab':'',
        'width':'',
        'height':'',
        'face':'0',
        'istype':'2',
        'qc':'',
        'nc':'1',
        'fr':'',
        'pn':pn,
        'rn':'30',
        'gsm':hex(pn)[2:],
        '1514425387405':''
    }
    url = url + urllib.parse.urlencode(queryString)
    return url
'''
百度图片在搜索的第一屏上，图片的地址是 objURL,图片的base64编码也在。
第n屏（n>=2)是通过XHR 动态加载，返回json数据，objURL是加密字符串
    秘钥是一个字符的对应关系，有2种映射：
    （1）多个字符映射为一个字符，'_z2C$q'=>':','_z&e3B'=>'.','AzdH3F'=>'/'。
    （2）单个字符映射为单字符。
'''

def decipherUrl(encryptUrl):
    decipherUrl = encryptUrl
    dictStr = {'_z2C$q':':', '_z&e3B':'.', 'AzdH3F':'/'}
    dictChar={
        'w' : 'a',  
        'k' : 'b',  
        'v' : 'c',  
        '1' : 'd',  
        'j' : 'e',  
        'u' : 'f',  
        '2' : 'g',  
        'i' : 'h',  
        't' : 'i',  
        '3' : 'j',  
        'h' : 'k',  
        's' : 'l',  
        '4' : 'm',  
        'g' : 'n',  
        '5' : 'o',  
        'r' : 'p',  
        'q' : 'q',  
        '6' : 'r',  
        'f' : 's',  
        'p' : 't',  
        '7' : 'u',  
        'e' : 'v',  
        'o' : 'w',  
        '8' : '1',  
        'd' : '2',  
        'n' : '3',  
        '9' : '4',  
        'c' : '5',  
        'm' : '6',  
        '0' : '7',  
        'b' : '8',  
        'l' : '9',  
        'a' : '0'
    }
    dictChar = {ord(key):value for key, value in dictChar.items()}
    for k, v in dictStr.items():
        decipherUrl = decipherUrl.replace(k, v)
    decipherUrl = decipherUrl.translate(dictChar)

    return decipherUrl

#pn是一个60为步长的等差数列。gsm看上去是16进制，转换成十进制，发现它就是pn值，试了也可以删掉。
def getImgInfos(keyword, pn):
    url = buildUrlForOtherPage(keyword, pn)
    r = requests.get(url)
    
    return r.json()['data']
    
  

def downloadImg(imgInfos):
    for info in imgInfos: #imgInfo是数组，每一个元素也是数组，一个是图片的URL，一个是图片类型
        if 'objURL' in info:
            url = decipherUrl(info['objURL'])
       
            try:
                r = requests.get(url)
            except:
                print("Get %s ERROR!" % url)
            
            filePath = "BaiduImages/" + info['di'] + "." + info['type']
            with open(filePath, 'wb') as f:
                f.write(r.content)
                f.close()
                print("Dowlaod %s is finish!" % (url))

            
def main():
    keyword = input("Enter the key word for download image:")
    for i in range(0,2):
        print("\t\tDownlaod No.{} page".format(i + 1))
        infos = getImgInfos(keyword, i * 30)
        downloadImg(infos)
        
    print("All images download FINISH!")


if __name__ == '__main__':
    main()
    
    
