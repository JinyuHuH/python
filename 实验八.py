import pandas as pd
import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline,Map


def get_data():
    df = pd.read_csv('E:\Wuhan-2019-nCoV.csv')  # 利用pandas读取数据
    df_province = df.loc[(df['date']>='2019-12-01')&(~df['province'].isnull())&(df['city'].isnull())] # 读取各省、自治区、直辖市历史数据
   # print(df_province)
    def transfer(x):
        if x.endswith('自治区') or x.endswith('省') or x.endswith('特别行政区') or x.endswith('市'):
            return x.replace('壮族', '').replace('维吾尔', '').replace('回族', '').replace('自治区', '').replace('省', '').replace(
                '特别行政区', '').replace('市', '')
        else:
            return x

    df_province['province'] = df_province['province'].apply(transfer) # 修改各省、自治区、直辖市的名称，以便map接收

    date = df_province['date'].unique().tolist()[:373] # 设置展示的天数2019.12.1-2020.12.8
    print(date)
    data_list = []
    time_list = []

    for i in date:
        time = i[0:].replace('-', '.')
        time_list.append(time)
        data = []
        name = df_province.loc[df_province['date'] == i]['province'].tolist()
        num = df_province.loc[df_province['date'] == i]['confirmed'].tolist()
        for x,y in zip(name,num):
            data.append({"name":x,"value":[y,x]})
        data_list.append({"time":time,"data":data})

    time_line(data_list,time_list)


def get_day_chart(data,day):#导入地图
    map_data = [
        [[x["name"], x["value"]] for x in d["data"]] for d in data if d["time"] == day
    ][0]
    map_chart = (
        Map()
            .add(
            series_name="",
            data_pair=map_data,
            maptype="china",
            label_opts=opts.LabelOpts(is_show=False),
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title="新冠疫情全国各省市发展趋势图",
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(255,255,255, 0.9)"
                ),
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
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="180",
                pos_top="center",
                is_piecewise=True,
                pieces=[
                    {'max': 9, 'min': 0, 'label': '0-9', 'color': '#FFFFCC'},
                    {'max': 99, 'min': 10, 'label': '10-99', 'color': '#FFC4B3'},
                    {'max': 999, 'min': 100, 'label': '100-999', 'color': '#FF9985'},
                    {'max': 9999, 'min': 1000, 'label': '1000-9999', 'color': '#F57567'},
                    {'max': 19999, 'min': 10000, 'label': '10000-19999', 'color': '#E64546'},
                    {'max': 29999, 'min': 20000, 'label': '20000-29999', 'color': '#B80909'},
                    {'max': 39999, 'min': 30000, 'label': '30000-39999', 'color': '#8A0808'},
                    {'max': 49999, 'min': 40000, 'label': '40000-49999', 'color': '#660000'},
                    {'max': 99999, 'min': 50000, 'label': '>=50000', 'color': '#660000'}
                ]
            ),
        )
    )

    return map_chart


def time_line(data,time_list):#设置时间轴
    timeline = Timeline(
        init_opts=opts.InitOpts(width="1570px", height="720px", theme=ThemeType.DARK)
    )
    for d in time_list:
        g = get_day_chart(data,d)
        timeline.add(g, time_point=d)

    timeline.add_schema(
        orient="vertical",#垂直
        is_auto_play=True,#自动播放
        is_inverse=True,#反向放置
        play_interval=5000,# 播放速度，单位ms
        pos_left="null",
        pos_right="12%",
        pos_top="20",
        pos_bottom="20",
        width="85",
        label_opts=opts.LabelOpts(is_show=True, color="#fff",interval=7),# interval 标签间隔
    )

    timeline.render('中国疫情发展趋势.html')


if __name__ == '__main__':
    get_data()
