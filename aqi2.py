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
        self.url = 'http://datacenter.mee.gov.cn/websjzx/dataproduct/airproduct/queryctiyaqipm.vm'
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':'139',
            'Content-Type':'application/x-www-form-urlencoded',
            # 'Cookie':'JSESSIONID=EEE2CF0F2B737F4BC091AE6D5CF7D7FD',
            'Host':'datacenter.mee.gov.cn',
            'Origin':'http://datacenter.mee.gov.cn',
            'Referer':'http://datacenter.mee.gov.cn/websjzx/dataproduct/airproduct/queryctiyaqipm.vm',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',

        }
        self.fp = open('./aqi2data.json','a',encoding='utf-8')

    def crawl(self):
        data = {
            "form['BIAOMINGCHENG']": "JCZZ.T_ENV_AUTO_CITYHOURAQI",
            "form['TYPEKEY']":"1",
            "pages": "1",
            "pageNum": "1",
            "pageSize": "400",
            "orderBy": "",
            "tempReportKey": "",
        }
        res = requests.post(url=self.url,headers=self.headers,data = data)
        # print(res.text)
        with open('./a.html','w',encoding='utf-8')as fp:
            fp.write(res.text)
        result = re.findall(r'<tr>\s+<td>\d+</td>\s+<td>(\d+-\d+-\d+)\s+(\d+)</td>\s+<td>(.*?)</td>\s+</td>\s+<td>(.*?)</td>\s+<td\s+class=".*?">(.*?)</td>\s+<td>(\d+)</td>\s+<td\s+title=".*?"\s+>(.*?)</td>\s+</tr>',res.text)
        print(result)
        print(len(result))
        tag = ['date','hour','province','city','AQL','AQI','pollutant']
        items = [dict(zip(tag,list(item))) for item in result]
        return items

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

