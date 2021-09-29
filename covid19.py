import csv

import requests # 数据爬虫库
import pandas as pd # 数据格式化库& 数据分析库
import json # 轻量化的数据交互格式
import time # 时间戳 1620614176806 ，从1970,0点0 至今 多少秒


# from pyecharts import options as opt
# from pyecharts.charts import Map


'''
  爬取COVID-19基础类
  args:url
'''
class GetCovid19Data():
    def __init__(self,url):
        self.url = url
    # 下载网页
    def download_html(self):
        response = requests.get(self.url)
        html = ""
        if response.status_code == 200:
            html = response.text
        return html

    # 解析网页
    def parser_html(self,html):
        data_json = json.loads(json.loads(html)['data'])['areaTree'][0]['children']
        lastUpdateTime = json.loads(json.loads(html)['data'])['lastUpdateTime']
        print(dict(json.loads(json.loads(html)['data'])))
        # print(type(data_json))
        prvince_datas = []

        for dt in data_json:
            data_dict = {}
            data_dict["province"] = dt['name']
            data_dict["nowConfirm"] = dt['total']['nowConfirm']
            data_dict["confirm"] = dt['total']['confirm']
            data_dict["suspect"] = dt['total']['suspect']
            data_dict["dead"] = dt['total']['dead']
            data_dict["heal"] = dt['total']['heal']
            data_dict["uptime"] = lastUpdateTime
            prvince_datas.append(data_dict)
        return pd.DataFrame(prvince_datas)




if __name__ == '__main__':
    base_url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&_={}"
    current_time = time.time()*1000 #当前时间戳
    crawl_url = base_url.format(current_time)
    covid19_data = GetCovid19Data(url=crawl_url)
    print(crawl_url)
    html = covid19_data.download_html()
    data = covid19_data.parser_html(html)
    print(data)
    provinces = data['province']
    nowConfirm = data['nowConfirm']
    data.to_csv('E:\\covid19')
    #
#    china_map = DrawMap.DrawMap()
 #   china_map.draw_china_map(province=provinces,nowConfirm=nowConfirm)







# # Step2：数据采集
# #   2.1: 目标网址
# base_url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&_={}"
# current_time = time.time()*1000 #当前时间戳
# crawl_url = base_url.format(current_time)
#
# #   2.2：发起请求，下载网页
# html = requests.get(crawl_url)
#
# html_status = html.status_code
# html_content =""
# if html_status == 200:
#     html_content = html.text
#
# # 2.3: 网页解析
# data_json = json.loads(json.loads(html_content)['data'])['areaTree'][0]['children']
# lastUpdateTime = json.loads(json.loads(html_content)['data'])['lastUpdateTime']
# # print(data_json)
# # print(type(data_json))
# prvince_datas = []
#
# for dt in data_json:
#     data_dict = {}
#     data_dict["province"] = dt['name']
#     data_dict["nowConfirm"] = dt['total']['nowConfirm']
#     data_dict["confirm"] = dt['total']['confirm']
#     data_dict["suspect"] = dt['total']['suspect']
#     data_dict["dead"] = dt['total']['dead']
#     data_dict["heal"] = dt['total']['heal']
#     data_dict["uptime"] = lastUpdateTime
#     prvince_datas.append(data_dict)
#
# # 2.4:保存数据
# df_data = pd.DataFrame(prvince_datas)
#
# df_data.to_csv('{}国内各省份疫情数据汇总'.format(time.strftime("%Y-%m-%d",time.localtime()))) # 20210510
#
# print("*"*20)
# print("download success!!!")