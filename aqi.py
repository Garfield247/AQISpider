# -*- coding: utf-8 -*-
# @Date    : 2018-12-20 10:54:14
# @Author  : LvGang/Garfield
# @Email   : Garfield_lv@163.com


import os
import re
import time
import json
import requests
from datetime import datetime

class AqiSpider(object):
    """docstring for AqiSpider"""
    def __init__(self):
        self.url = 'http://106.37.208.228:8082/Home/Default?_={timestr}'
        self.headers = {
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'en-US,en;q=0.9',
            'Connection':'keep-alive',
            'Host':'106.37.208.228:8082',
            'Referer':'http://106.37.208.228:8082/',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
        }
        self.fp = open('./sqidata.json','a',encoding='utf-8')

    def crawl(self):
        r = requests.get(url=self.url.format(timestr=str(time.time()).replace('.','')[0:-4]),headers=self.headers)
        res = json.loads(re.findall(r'var cities = \[(\[.*?\])\]\[0\]',r.text)[0])
        print(res)
        return res

    def save_data(self,item):
        data = json.dumps(item,ensure_ascii=False)
        self.fp.write(data+'\n')


    def main(self):
        items = self.crawl()
        for item in items:
            item['DateTime'] = str(datetime.now().date())
            self.save_data(item)



if __name__ == '__main__':
    aqi = AqiSpider()
    aqi.main()

