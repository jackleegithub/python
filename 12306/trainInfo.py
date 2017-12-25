'''
#从12306的余票查询中，获取各个车次的信息
#由于返回的JSON 数据简单加密，需要与网页的数据对照
#r.json()['data']['result'] 返回的是一个数组，一个元素保存着一个车次的数据，例如历时、车票等信息
'''

trainInfo = {
    '车次':3,
    '始发站':4,
    '终点站':5,
    '出发地':6,
    '目的地':7,
    '出发时间':8,
    '到达时间':9,
    '历时':10,
    '出发日':13,
    '高级软卧':21,
    '软卧':23,
    '无座':26,
    '硬卧':28,
    '硬座':29,
    '二等座':30,
    '一等座':31,
    '商务座特等座':32,
    '动卧':33
}