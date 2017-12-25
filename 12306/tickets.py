# coding: utf-8

"""命令行火车票查看器

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets 北京 上海 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""

import prettytable
import requests
from docopt import docopt
from stations import stations

def getTrainsInfo(fromStation, toStation, trainsInfo):
    header = '车次 车站 时间 历时 一等 二等 软卧 硬卧 硬座 无座 查询时间'.split()
    pt = prettytable.PrettyTable()
    pt._set_field_names(header)

    data = trainsInfo['data']
    datas = data['result'] # is a array
    dataIndex = [3,6,7,8,9,10,31,30,23,28,29,26,13]

    for data in datas:
        row =[]
        lsContent = data.split('|')

        row.append(lsContent[3])
        row.append("{}/{}".format(fromStation, toStation))
        row.append("{}/{}".format(lsContent[8], lsContent[9]))
        for i in dataIndex[5:]:
            row.append(lsContent[i])
        pt.add_row(row)
    
    return pt


def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    fromStation = stations.get(arguments['<from>'])
    toStation = stations.get(arguments['<to>'])
    date = arguments['<date>']

    url ='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
        date, fromStation, toStation)
    r = requests.get(url)
    pt = getTrainsInfo(arguments['<from>'], arguments['<to>'], r.json())
    print(pt)


if __name__ == '__main__':
    cli()
