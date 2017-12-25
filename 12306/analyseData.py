#从12306的余票查询中，获取各个车次的信息
#由于返回的JSON 数据简单加密，需要与网页的数据对照
#r.json()['data']['result'] 返回的是一个数组，一个元素保存着一个车次的数据，例如历时、车票等信息
'''
for info in r.json()['data']['result']
    lsInfo = info.split("|")
    数组下标,代表信息
    3,车次
    4,始发站
    5,终点站
    6,出发地
    7,目的地
    8,出发时间
    9,到达时间
    10,历时
    13,出发日
    21,高级软卧
    23,软卧
    26,无座
    29,硬座
    28,硬卧
    30,二等座
    31,一等座
    32,商务座特等座
    33,动卧
'''
import requests
from trainInfo import trainInfo
import prettytable


header = '车次 车站 时间 历时 一等座 二等座 软卧 硬卧 硬座 无座'.split()
pt = prettytable.PrettyTable()
pt._set_field_names(header)


url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-12-26&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=CSQ&purpose_codes=ADULT'
    
r = requests.get(url)
data = r.json()['data']
datas = data['result'] # is a array
dataIndex = [3,6,7,8,9,10,31,30,23,28,29,26]

for data in datas:
    row =[]
    lsContent = data.split('|')

    #info ="{}-{}/{}-{}/{}-{}-{}-{}-{}-{}-{}-{}".format(
            #lsContent[3], lsContent[6],lsContent[7],lsContent[8],lsContent[9],lsContent[10],
            #lsContent[31],lsContent[30],lsContent[23],lsContent[28],lsContent[29],lsContent[26])
    row.append(lsContent[3])
    row.append("{}/{}".format(lsContent[6], lsContent[7]))
    row.append("{}/{}".format(lsContent[8], lsContent[9]))
    for i in dataIndex[5:]:
        row.append(lsContent[i])
    pt.add_row(row)
print(pt)
    
    
      
