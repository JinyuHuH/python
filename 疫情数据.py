import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
    }
#省级正则表达式
provinceName_re = re.compile(r'"provinceName":"(.*?)",')
provinceShortName_re = re.compile(r'"provinceShortName":"(.*?)",')
currentConfirmedCount_re = re.compile(r'"currentConfirmedCount":(.*?),')
confirmedCount_re = re.compile(r'"confirmedCount":(.*?),')
suspectedCount_re = re.compile(r'"suspectedCount":(.*?),')
curedCount_re = re.compile(r'"curedCount":(.*?),')
deadCount_re = re.compile(r'"deadCount":(.*?),')
comment_re = re.compile(r'"comment":"(.*?)",')
locationId_re = re.compile(r'"locationId":(.*?),')
statisticsData_re = re.compile(r'"statisticsData":"(.*?)",')
cities_re = re.compile(r'"cities":\[\{(.*?)\}\]')

#市级正则表达式
cityName_re = re.compile(r'"cityName":"(.*?)",')
currentConfirmedCount_1_re = re.compile(r'"currentConfirmedCount":(.*?),')
confirmedCount_1_re = re.compile(r'"confirmedCount":(.*?),')
suspectedCount_1_re = re.compile(r'"suspectedCount":(.*?),')
curedCount_1_re = re.compile(r'"curedCount":(.*?),')
deadCount_1_re = re.compile(r'"deadCount":(.*?),')
locationId_1_re = re.compile(r'"locationId":(.*?)\},')

#爬虫爬取数据
datas = requests.get(url,headers = headers)
datas.encoding = 'utf-8'
soup = BeautifulSoup(datas.text,'lxml')
data = soup.find_all('script',{'id':'getAreaStat'})
data = str(data)
data_str = data[54:-23]

#替换字符串内容，避免重复查找
citiess = re.sub(cities_re,'8888',data_str)
#查找省级数据
provinceNames = re.findall(provinceName_re,citiess)
provinceShortNames = re.findall(provinceShortName_re,citiess)
currentConfirmedCounts = re.findall(currentConfirmedCount_re,citiess)
confirmedCounts = re.findall(confirmedCount_re,citiess)
suspectedCounts = re.findall(suspectedCount_re,citiess)
curedCounts = re.findall(curedCount_re,citiess)
deadCounts = re.findall(deadCount_re,citiess)
comments = re.findall(comment_re,citiess)
locationIds = re.findall(locationId_re,citiess)
statisticsDatas = re.findall(statisticsData_re,citiess)


#查找市级数据
citiess_str1 = re.findall(cities_re,data_str)
#将市级列表数据转为字符串，方便正则表达式查找
citiess_str = str(citiess_str1)
cityName = re.findall(cityName_re,citiess_str)
currentConfirmedCount_1 = re.findall(currentConfirmedCount_1_re,citiess_str)
confirmedCount_1 = re.findall(confirmedCount_1_re,citiess_str)
suspectedCount_1 = re.findall(suspectedCount_1_re,citiess_str)
curedCount_1 = re.findall(curedCount_1_re,citiess_str)
deadCount_1 = re.findall(deadCount_1_re,citiess_str)

# 省级数据转换为pandas数组
df = {
    '地区代码':pd.Series(locationIds),
    '省':pd.Series(provinceNames),
    '省区短名':pd.Series(provinceShortNames),
    '当前确诊':pd.Series(currentConfirmedCounts),
    '累计确诊':pd.Series(confirmedCounts),
    '疑似确诊':pd.Series(suspectedCounts),
    '治愈人数':pd.Series(curedCounts),
    '死亡人数':pd.Series(deadCounts),
    '评论':pd.Series(comments),
    '统计数据区':pd.Series(statisticsDatas),
}
pds = pd.DataFrame(df)
pds.to_excel('E:\\国内疫情统计表.xlsx',index=True)





