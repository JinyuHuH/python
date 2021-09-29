import pandas as pd
import pyodbc
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
# bar-柱状图 pie-饼图/玫瑰图 map-地图 line-折线图 radar-雷达图 scatter-散点图  Overlap-柱折合并 funnel-漏斗图 Liquid-水滴图
# page-拼合所有图表
from pyecharts.charts import *
from bs4 import BeautifulSoup
from pyecharts.globals import ThemeType

conn = pyodbc.connect(DRIVER='{SQL Server}', SERVER='localhost', DATABASE='AirData', UID="chinaair", PWD="chinaair")
data = pd.read_sql("select * from 全国空气质量", con=conn)
data.columns=['日期','质量等级','AQI指数','当天AQI排名','PM2.5','PM10','So2','No2','Co','O3','省份']
#print(data)
# data = pd.read_csv('E:\可视化大屏\全国空气质量.csv', encoding='gbk')

#动态地图
df=pd.read_csv(r'E:\可视化大屏\全国空气质量.csv',encoding='gbk')  # 利用pandas读取数据

date = df['日期'].unique().tolist()[:366] # 设置展示的天数
#print(date)
data_list = []
time_list = []

for i in date:
    time = i[0:].replace('-', '.')
    time_list.append(time)
    dt = []
    name = df.loc[df['日期'] == i]['省份'].tolist()
    num = df.loc[df['日期'] == i]['AQI指数'].tolist()
    for x,y in zip(name,num):
        dt.append({"name":x,"value":[y,x]})
    data_list.append({"time":time,"data":dt})



def get_day_chart(data,day):#导入地图
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == day
    ][0]
    map_chart = (
        Map()
            .add(
            series_name="AQI指数",
            data_pair=map_data,
            maptype="china",
            label_opts=opts.LabelOpts(is_show=False),#显示省份名称
            is_map_symbol_show=False,
            #itemstyle_opts={
             #   "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
              #  "emphasis": {
               #     "label": {"show": Timeline},
                #    "areaColor": "rgba(255,255,255, 0.5)",
                #},},
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                #title="新冠疫情全国各省市发展趋势图",
                pos_left="center",
                pos_top="top",
               # title_textstyle_opts=opts.TextStyleOpts(
                #    font_size=25, color="rgba(255,255,255, 0.9)"),
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[1] + ': ' + params.data.value[0];
                    }
                }"""
                ),
            ),
            #设置图例
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="220",
                is_piecewise=True,
                pieces=[
                    {'max': 15, 'min': 0, 'label': '0-15', 'color': '#0066FF'},
                    {'max': 30, 'min': 15, 'label': '15-30', 'color': '#33CCCC'},
                    {'max': 45, 'min': 30, 'label': '30-45', 'color': '#0099CC'},
                    {'max': 60, 'min': 45, 'label': '45-60', 'color': '#99CCFF'},
                    {'max': 75, 'min': 60, 'label': '60-75', 'color': '#77DDFF'},
                    {'max': 90, 'min': 75, 'label': '75-90', 'color': '#FFCC99'},
                    {'max': 105, 'min': 90, 'label': '90-105', 'color': '#FFCC66'},
                    {'max': 120, 'min': 105, 'label': '105-120', 'color': '#FFAA33'},#FF9933
                    {'max':135,'min': 120, 'label': '120-135', 'color': '#FF7F50 '},
                    { 'min': 135, 'label': '135+', 'color': '#FF5511'}
                ]
            ),
        )
    )

    return map_chart


#设置时间轴
timeline = Timeline(init_opts=opts.InitOpts(theme=ThemeType.ESSOS)).add_schema(
    orient="vertical",#垂直
    is_auto_play=True,#自动播放
    is_inverse=True,#反向放置
    #play_interval=1000000000,# 播放速度，单位ms
    pos_left="null",
    pos_right="0",
    pos_top="10",
    pos_bottom="20",
    width="85",
    label_opts=opts.LabelOpts(is_show=True,interval=7))


for d in time_list:
    g = get_day_chart(data_list,d)
    timeline.add(g, time_point=d)



# 静态地图热力
aqi = data[['省份', 'AQI指数']].copy()
aqi['总aqi'] = aqi['AQI指数'].groupby(aqi['省份']).cumsum()
last_aqi = aqi.drop_duplicates(subset=['省份'], keep='last')
last_aqi['平均aqi'] = round(last_aqi['总aqi'] / len(data[data['省份'] == '北京'].value_counts()), 2)
heatmap_data = last_aqi[['省份', '平均aqi']].values.tolist()
# print(last_aqi)
map = Map(init_opts=opts.InitOpts(theme=ThemeType.ESSOS)).add(series_name="AQI指数",  # 设置提示框标签
                                                              data_pair=heatmap_data,  # 输入数据
                                                              maptype="china",  # 设置地图类型为中国地图
                                                              is_map_symbol_show=False)  # 不显示标记点
# 设置系列配置项
map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示省份（标签）名称
# 设置全局配置项
map.set_global_opts(  # title_opts=opts.TitleOpts(title="中国各地累计确诊人数地图"),
    # 设置视觉映射配置项
    legend_opts=opts.LegendOpts(is_show=False),  # 66CCFF
    visualmap_opts=opts.VisualMapOpts(pieces=[  # 自定义分组的分点和颜色
        {'max': 30, 'min': 15, 'label': '15-30', 'color': '#0099CC'},
        {'max': 45, 'min': 30, 'label': '30-45', 'color': '#99CCFF'},
        {'max': 60, 'min': 45, 'label': '45-60', 'color': '#FFCC99'},
        {'max': 75, 'min': 60, 'label': '60-75', 'color': '#FFCC66'},
        {'max': 85, 'min': 75, 'label': '75-85', 'color': '#FF9933'},
        {'min': 85, 'label': '85+', 'color': '#FF5511'}

    ],
        is_piecewise=True))

# 玫瑰图
data1 = data[data['质量等级'] == '优']
data2 = data[data['质量等级'] == '良']
data3 = data[data['质量等级'] == '轻度污染']
data4 = data[data['质量等级'] == '中度污染']
data5 = data[data['质量等级'] == '重度污染']
data6 = data[data['质量等级'] == '严重污染']
case = pd.DataFrame()
case['质量等级'] = ['优', '良', '轻度污染', '中度污染', '重度污染', '严重污染']
case['次数'] = [data1['质量等级'].count(), data2['质量等级'].count(), data3['质量等级'].count(), data4['质量等级'].count(),
              data5['质量等级'].count(), data6['质量等级'].count()]
df = case[['质量等级', '次数']].sort_values(by='次数', ascending=False).values
pie = Pie(init_opts=opts.InitOpts(theme=ThemeType.ESSOS)).add("质量等级",
                                                              df,  # 输入数据
                                                              radius=["25%", "65%"],  # 设置内半径和外半径
                                                              center=["55%", "55%"],  # 设置圆心位置左，上
                                                              rosetype="radius",  # 玫瑰图模式，通过半径区分数值大小，角度大小表示占比
                                                              )

pie.set_global_opts(  # title_opts=opts.TitleOpts(title="全国空气质量玫瑰图", pos_right='50%'),  # 图标题的位置
    legend_opts=opts.LegendOpts(  # 设置图例
        orient='vertical',  # 垂直放置图例
        pos_right="85%",  # 设置图例位置
        pos_top="25%"))
pie.set_colors(['#33CCCC', '#66CCFF', '#0099CC', '#006699'])  # 图的颜色
pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b} : {d}%", color='white'))

# 漏斗图
funnel = (Funnel(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
          .add("全国总天数", df,
               sort_='descending',
               label_opts=opts.LabelOpts(position="inside"))
          # .set_global_opts(title_opts=opts.TitleOpts(title=" ", subtitle="标题"))
          )
funnel.render('漏斗.html')
# 横行条形图
city = last_aqi[['省份', '平均aqi']].sort_values(by='平均aqi', ascending=False)  # 降序排列
citymax = city[0:5].values
citymin = city[-5:32].values
citymaxdata = list(citymax[:, 0])
aqimaxdata = list(citymax[:, 1])
citymindata = list(citymin[:, 0])
aqimindata = list(citymin[:, 1])

bar1 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
        .add_xaxis(citymaxdata)
        .add_yaxis("平均AQI指数", aqimaxdata)
        .reversal_axis()
        .set_colors(['#66CCFF'])
        .set_global_opts(  # title_opts=opts.TitleOpts("rever"),
        toolbox_opts=opts.ToolboxOpts(is_show=True))
        .set_series_opts(title_opts=opts.TitleOpts(title='biaoti'), label_opts=opts.LabelOpts(position="right"))
)
bar2 = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
        .add_xaxis(citymindata)
        .add_yaxis("平均AQI指数", aqimindata)
        .reversal_axis()
        .set_colors(['#33CCCC'])
        .set_global_opts(  # title_opts=opts.TitleOpts("rever"),
        toolbox_opts=opts.ToolboxOpts(is_show=True))
        .set_series_opts(title_opts=opts.TitleOpts(title='biaoti'), label_opts=opts.LabelOpts(position="right"))
)
bar1.render('条1.html')
bar2.render('条2.html')
# 折线图
item1 = data[(data['日期'] >= '2020-01-01') & (data['日期'] <= '2020-01-31')]
item2 = data[(data['日期'] >= '2020-02-01') & (data['日期'] <= '2020-02-29')]
item3 = data[(data['日期'] >= '2020-03-01') & (data['日期'] <= '2020-03-31')]
item4 = data[(data['日期'] >= '2020-04-01') & (data['日期'] <= '2020-04-30')]
item5 = data[(data['日期'] >= '2020-05-01') & (data['日期'] <= '2020-05-31')]
item6 = data[(data['日期'] >= '2020-06-01') & (data['日期'] <= '2020-06-30')]
item7 = data[(data['日期'] >= '2020-07-01') & (data['日期'] <= '2020-07-31')]
item8 = data[(data['日期'] >= '2020-08-01') & (data['日期'] <= '2020-08-31')]
item9 = data[(data['日期'] >= '2020-09-01') & (data['日期'] <= '2020-09-30')]
item10 = data[(data['日期'] >= '2020-10-01') & (data['日期'] <= '2020-10-31')]
item11 = data[(data['日期'] >= '2020-11-01') & (data['日期'] <= '2020-11-30')]
item12 = data[(data['日期'] >= '2020-12-01') & (data['日期'] <= '2020-12-31')]
#print(item2)
pm25 = item1['PM2.5'].mean(), item2['PM2.5'].mean(), item3['PM2.5'].mean(), item4['PM2.5'].mean(), item5[
    'PM2.5'].mean(), item6['PM2.5'].mean(), item7['PM2.5'].mean(), item8['PM2.5'].mean(), item9['PM2.5'].mean(), item10[
           'PM2.5'].mean(), item11['PM2.5'].mean(), item12['PM2.5'].mean()
pm10 = item1['PM10'].mean(), item2['PM10'].mean(), item3['PM10'].mean(), item4['PM10'].mean(), item5['PM10'].mean(), \
       item6['PM10'].mean(), item7['PM10'].mean(), item8['PM10'].mean(), item9['PM10'].mean(), item10['PM10'].mean(), \
       item11['PM10'].mean(), item12['PM10'].mean()
so2 = item1['So2'].mean(), item2['So2'].mean(), item3['So2'].mean(), item4['So2'].mean(), item5['So2'].mean(), item6[
    'So2'].mean(), item7['So2'].mean(), item8['So2'].mean(), item9['So2'].mean(), item10['So2'].mean(), item11[
          'So2'].mean(), item12['So2'].mean()
no2 = item1['No2'].mean(), item2['No2'].mean(), item3['No2'].mean(), item4['No2'].mean(), item5['No2'].mean(), item6[
    'No2'].mean(), item7['No2'].mean(), item8['No2'].mean(), item9['No2'].mean(), item10['No2'].mean(), item11[
          'No2'].mean(), item12['No2'].mean()
co = item1['Co'].mean(), item2['Co'].mean(), item3['Co'].mean(), item4['Co'].mean(), item5['Co'].mean(), item6[
    'Co'].mean(), item7['Co'].mean(), item8['Co'].mean(), item9['Co'].mean(), item10['Co'].mean(), item11['Co'].mean(), \
     item12['Co'].mean(),
o3 = item1['O3'].mean(), item2['O3'].mean(), item3['O3'].mean(), item4['O3'].mean(), item5['O3'].mean(), item6[
    'O3'].mean(), item7['O3'].mean(), item8['O3'].mean(), item9['O3'].mean(), item10['O3'].mean(), item11['O3'].mean(), \
     item12['O3'].mean(),

line = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
        .add_xaxis(['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'])
        .add_yaxis('PM2.5', [round(i, 2) for i in pm25], is_smooth=True, is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='average', name='均值'),
                                                           opts.MarkPointItem(type_='max', name='最大值'),
                                                           opts.MarkPointItem(type_='min', name='最小值')],
                                                     symbol_size=40))  # 平滑
        .add_yaxis('PM10', [round(i, 2) for i in pm10], is_smooth=True, is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='average', name='均值'),
                                                           opts.MarkPointItem(type_='max', name='最大值'),
                                                           opts.MarkPointItem(type_='min', name='最小值')],
                                                     symbol_size=40))
        .add_yaxis('So2', [round(i, 2) for i in so2], is_smooth=True, is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='average', name='均值'),
                                                           opts.MarkPointItem(type_='max', name='最大值'),
                                                           opts.MarkPointItem(type_='min', name='最小值')],
                                                     symbol_size=40))
        .add_yaxis('No2', [round(i, 2) for i in no2], is_smooth=True, is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='average', name='均值'),
                                                           opts.MarkPointItem(type_='max', name='最大值'),
                                                           opts.MarkPointItem(type_='min', name='最小值')],
                                                     symbol_size=40))
        .add_yaxis('Co', [round(i, 2) for i in co], is_smooth=True, is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='average', name='均值'),
                                                           opts.MarkPointItem(type_='max', name='最大值'),
                                                           opts.MarkPointItem(type_='min', name='最小值')],
                                                     symbol_size=40))
        .add_yaxis('O3', [round(i, 2) for i in o3], is_smooth=True, is_symbol_show=False,
                   markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='average', name='均值'),
                                                           opts.MarkPointItem(type_='max', name='最大值'),
                                                           opts.MarkPointItem(type_='min', name='最小值')],
                                                     symbol_size=40))
        .set_series_opts(title_opts=opts.TitleOpts(title='各项指标每月变化情况'))
)
line.render('折线.html')
# 散点图
Pm25max, Pm25min = data['PM2.5'].max(), data['PM2.5'].min()
Pm10max, Pm10min = data['PM10'].max(), data['PM10'].min()
So2max, So2min = data['So2'].max(), data['So2'].min()
No2max, No2min = data['No2'].max(), data['No2'].min()
Comax, Comin = data['Co'].max(), data['Co'].min()
O3max, O3min = data['O3'].max(), data['O3'].min()
# print(Pm25max,Pm25min)
max = Pm25max, Pm10max, So2max, No2max, Comax, O3max
min = Pm25min, Pm10min, So2min, No2min, Comin, O3min
# print(min)
x = ['PM2.5', 'PM10', 'So2', 'No2', 'Co', 'O3']
scatter = (EffectScatter(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
    .add_xaxis(x)
    .add_yaxis("最大", max)#, color='#FFD700'
    .add_yaxis("最小", min)#, color='#78ff33'
    .set_global_opts(
    # title_opts=opts.TitleOpts(title="各项指标最大最小值展示"),
    visualmap_opts=opts.VisualMapOpts(
        type_="size",  # 映射大小
        max_=1100,
        min_=0),
))
scatter.render('气泡.html')
# 水滴图
total = data['AQI指数'].count()  # 11162
pro1 = data[data['AQI指数'] <= 50]['AQI指数'].count() / total
pro2 = data[(data['AQI指数'] > 50) & (data['AQI指数'] <= 100)]['AQI指数'].count() / total
pro3 = data[data['AQI指数'] > 100]['AQI指数'].count() / total
# print(pro3)
liquid1 = Liquid(init_opts=opts.InitOpts(theme=ThemeType.ESSOS)).add('AQI:0-50',
                                                                     data=[pro1],  # 每个波浪的位置
                                                                     shape='roundRect',
                                                                     color=['#5CACEE'],  # 波浪颜色，序列
                                                                     is_animation=True,  # 显示波浪动画
                                                                     is_outline_show=False,  # 显示边框
                                                                     # 球在画布上的位置
                                                                     center=['20%', '50%'],
                                                                     label_opts=opts.LabelOpts(font_size=30,
                                                                                               color='black',
                                                                                               position='inside')
                                                                     # 30%显示的颜色和位置
                                                                     )
liquid2 = Liquid(init_opts=opts.InitOpts()).add('AQI:50-100',
                                                data=[pro2],  # 每个波浪的位置
                                                shape='roundRect',
                                                color=['#5CACEE'],  # 波浪颜色，序列
                                                is_animation=True,  # 显示波浪动画
                                                is_outline_show=False,  # 显示边框
                                                # 球在画布上的位置
                                                center=['50%', '50%'],
                                                label_opts=opts.LabelOpts(font_size=30, color='black',
                                                                          position='inside')  # 30%显示的颜色和位置
                                                )
liquid3 = Liquid(init_opts=opts.InitOpts()).add('AQI:100+',
                                                data=[pro3],  # 每个波浪的位置
                                                shape='roundRect',
                                                color=['#5CACEE'],  # 波浪颜色，序列
                                                is_animation=True,  # 显示波浪动画
                                                is_outline_show=False,  # 显示边框
                                                # 球在画布上的位置
                                                center=['50%', '50%'],
                                                label_opts=opts.LabelOpts(font_size=30, color='black',
                                                                          position='inside')  # 30%显示的颜色和位置
                                                )

# 雷达图
radar = (
    Radar(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
        .add_schema(
        # 各项的max_值可以不同
        schema=[
            opts.RadarIndicatorItem(name='PM2.5', max_=1000),
            opts.RadarIndicatorItem(name='PM10', max_=1100),
            opts.RadarIndicatorItem(name='So2', max_=100),
            opts.RadarIndicatorItem(name='No2', max_=150),
            opts.RadarIndicatorItem(name='Co', max_=10),
            opts.RadarIndicatorItem(name='O3', max_=300),
        ]
    )
        .add('max', [max],
             color='#FFBB66',
             areastyle_opts=opts.AreaStyleOpts(  # 设置填充的属性
                 opacity=0.5,
                 color='#FFBB66'
             ), )
        .add('min', [min],
             color='#ADD8E6',
             areastyle_opts=opts.AreaStyleOpts(
                 opacity=0.5,  # 透明度
                 color='#ADD8E6'
             ), )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    # .set_global_opts(title_opts=opts.TitleOpts(title='款色码质价影响'))
)
radar.render('雷达.html')
#文本框
daydata = (Pie().set_global_opts(title_opts=opts.TitleOpts(title='监控天数：366天',
                                                           pos_top='15%', pos_left='center',
                                                           subtitle='\t\t\t\t\t\t\t\t\t\t\t\t\n起止时间：2020.1.1-2020.12.31',
                                                           item_gap=1,
                                                           title_textstyle_opts=opts.TextStyleOpts(color="#00FFFF",font_size=30),
                                                           subtitle_textstyle_opts=opts.TextStyleOpts(color="#00BFFF")
                                                           )))

daydata.render('字.html')
#拼合图表
page = (Page().add(pie).add(timeline).add(funnel).add(bar1).add(bar2).add(line).add(scatter).add(liquid1).add(liquid2).add(
    liquid3).add(radar).add(daydata))
page.render('空气数据.html')

with open("空气数据.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    #                   宽度：500px；高度：250像素；   位置：绝对；     顶部：50像素；左：0px；  边框样式：直线；      边框颜色：#444444；     边框-宽度：3px；
    divs[0]["style"] = "width:550px;height:280px;position:absolute;top:250px;left:20px;"  # 玫瑰图
    #divs[1]['style'] = "width:670px;height:470px;position:absolute;top:100px;left:600px;"  # 地图
    divs[1]['style'] = "width:750px;height:480px;position:absolute;top:150px;left:600px;"  # 地图
    divs[2]["style"] = "width:520px;height:290px;position:absolute;top:20px;left:1380px;"  # 漏斗图
    divs[3]["style"] = "width:450px;height:260px;position:absolute;top:660px;left:600px;"  # 条1
    divs[4]["style"] = "width:450px;height:260px;position:absolute;top:660px;left:1080px;"  # 条2
    divs[5]["style"] = "width:550px;height:360px;position:absolute;top:560px;left:20px;"  # 折线图
    divs[6]["style"] = "width:520px;height:290px;position:absolute;top:340px;left:1380px;"  # 散点图
    divs[7]["style"] = "width:550px;height:200px;position:absolute;top:20px;left:20px;"  # 水滴1
    divs[8]["style"] = "width:300px;height:200px;position:absolute;top:20px;left:130px;"  # 水滴2
    divs[9]["style"] = "width:300px;height:200px;position:absolute;top:20px;left:280px;"  # 水滴3
    divs[10]["style"] = "width:340px;height:260px;position:absolute;top:660px;left:1560px;"  # 雷达图
    divs[11]['style'] = "width:250px;height:100px;position:absolute;top:70px;left:615px;"#文本
    body = html_bf.find("body")
    body["style"] = "background-color:rgb(91 92 110);background-image:url('1.jpg');background-size:100%;"
    div_title = "<div align=\"center\" style=\"width:1840px;\">\n<span style=\"font-size:45px;font face=\'黑体\';color:#FFFFFF\"><b>2020年全国空气质量数据显示</b></div>"
    # 修改页面背景色、追加标题
    body.insert(0, BeautifulSoup(div_title, "lxml").div)
    html_new = str(html_bf)
    html.seek(0, 0)
    html.truncate()
    html.write(html_new)
    html.close()
