#通过 js 文件 https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9035
#获取 车子名（汉字）和 英文代码的对应关系。
import re
import requests
import pprint


url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9035'
r = requests.get(url)
p = re.compile(r'([\u4e00-\u9fa5]+)\|([A-Z]+)')
ls = re.findall(p, r.text)
pprint.pprint(dict(ls), indent=4)
