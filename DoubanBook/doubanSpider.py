'''
    爬取豆瓣图书信息
    索引页：https://www.douban.com/tag/%E5%8C%97%E4%BA%AC/book?start=15
    详细页：在索引页可以查到

    豆瓣有饭爬虫，有较多的异常处理和状态判断
'''
import requests
from bs4 import BeautifulSoup
import urllib
import re
from openpyxl import Workbook

def getBookUrls(tag, page = 0):
    url = 'https://www.douban.com/tag/' + urllib.parse.urlencode({tag:""})[:-1] + "/book?start=" + str(int(page) * 15)

    try:
        r = requests.get(url)
    except:
        print("Get {} book ERROR!".format(tag))
        return []
    if r.status_code != requests.codes.ok:
        print("Get book of {} occur ERROR!".format(tag))
        return {}
        
    soup = BeautifulSoup(r.text, "html.parser")

    if soup.title.string == "页面不存在":
        print("The page of book of {} is NOT EXIST!".format(nameUrl[0]))
        return []
    div = soup.find("div", class_ = "mod book-list")

    #[[name, url], [name, url] ... ]
    nameAndUrls =[[a.string, a["href"]] for a in div.find_all("a", class_ = "title")]

    return nameAndUrls

#通过书名和链接 获取图书的详细信息
def getBookDetialByNameAndUrl(nameUrl):
    if nameUrl:
        try:
            r = requests.get(nameUrl[1])
        except:
            print("Get book of {} occur ERROR!".format(nameUrl[0]))
            return {}
        
        try:
            soup = BeautifulSoup(r.text, "html.parser")
        except:
            print("Parse book of {} occur ERROR!".format(nameUrl[0]))
            return {}
        if soup.title.string == "页面不存在":
            print("The page of book of {} is NOT EXIST!".format(nameUrl[0]))
            return {}
        
        info ={} #保存输的各种信息
        info["name"] = nameUrl[0] #书名
        
        if soup.find("span", class_="pl"):
            if re.search(r"作者",soup.find("span", class_="pl").string) == None:
                author =""
                spans = soup.find("div", id="info").find_all("span", class_="pl")
            else:
                author = re.sub(r"\s*", "", soup.find("span", class_="pl").next_sibling.next_element.string) #作者
                spans = soup.find("div", id="info").find_all("span", class_="pl")[1:]
        else:
            author = ""
        info["author"] = author
        
        
        for i in spans:
            info[i.string[:-1]] = i.next_sibling.strip() #其它信息

        if soup.find("strong", class_="ll rating_num "):
            rating = soup.find("strong", class_="ll rating_num ").string.strip()
        else:
            rating = ""
        info["rating"] = rating

        if soup.find("span", property="v:votes"):
            people = soup.find("span", property="v:votes").string#评价人数
        else:
            people = ""
        info["people"] = people
        
        return info
    else:
        return {}
    
    

def saveInfo2Excel():
    pass

wb = Workbook()
ws = wb.active
sequence = 1
tag = input("Enter the tag about book:")
ws.append(['序号','书名','评分','评价人数','作者','出版社'])
for index in range(10):
    print("Get No.{} page books infomation about {}.".format(index + 1, tag))
    for nu in getBookUrls(tag, index):
        print("\tGet {} infomation at {}.".format(nu[0], nu[1]))
        info =getBookDetialByNameAndUrl(nu)
        if info:
            if "出版社" in info:
                press = info["出版社"]
            else:
                press = ""
            ws.append([sequence, info["name"], info["rating"], info["people"], info["author"], press])

        sequence += 1
try:        
    wb.save("douban.xlsx")
except:
    print("Save excel file ERROR!")

