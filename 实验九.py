import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map3D
from pyecharts.globals import ChartType

def city_data(df):
    sheet_names = ['Table ' + str(x) for x in range(1, 77)]
    for st_name in sheet_names:
        data = pd.read_excel(r'E:\\数据可视化\\全国城市经纬度汇总.xlsx', sheet_name=st_name, names=['省份', '地市', '区县', '经度', '纬度'])

        def make(x):
            if x.endswith('市'):
                return x.replace('市', '')
            else:
                return x

        data['区县'] = data['区县'].apply(make)

    df['出发经度'] = df['出发城市'].replace(data['区县'].values, data['经度'].values)
    df['出发纬度'] = df['出发城市'].replace(data['区县'].values, data['纬度'].values)
    df['到达经度'] = df['到达城市'].replace(data['区县'].values, data['经度'].values)
    df['到达纬度'] = df['到达城市'].replace(data['区县'].values, data['纬度'].values)
    #print(df)
    linedata = []
    for i in range(len(df)):
        go_data = [df["出发经度"][i], df["出发纬度"][i]]
        arr_data = [df["到达经度"][i], df["到达纬度"][i]]
        linedata.append([go_data, arr_data])
    return linedata

def china_map(linedata):
    c = (
        Map3D()
            .add_schema(
            maptype="china",  # 地图类型
            itemstyle_opts=opts.ItemStyleOpts(  # 图元配置项
                color="rgb(5,101,123)",
                opacity=1,  # 图形透明度
                border_width=0.8,
                border_color="rgb(62,215,213)",
            )

        )
            .add(
            series_name="",
            data_pair=linedata,
            type_=ChartType.LINES3D,  # 叠加图的类型 lines3D
            effect=opts.Lines3DEffectOpts(  # 飞线的尾迹特效
                is_show=True,
                period=4,  # 尾迹特效周期
                trail_width=3,  # 尾迹
                trail_length=0.5,
                trail_color="#f00",
                trail_opacity=1,
            ),
            linestyle_opts=opts.LineStyleOpts(is_show=False, color="#fff", opacity=0),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Map3D-Lines3D"))
            .render("lines3d.html")
    )


def air_data():
    data = pd.read_csv(r'E:\数据可视化\航班动态算法大赛原始数据\训练集\2015年5月到2017年5月航班动态数据.csv', encoding='gbk')
    df = data[data['航班是否取消'] == '正常'].head(50)
    air = pd.read_excel(r'E:\数据可视化\航班动态算法大赛原始数据\训练集\机场城市对应表.xlsx')
    df['出发城市'] = df['出发机场'].replace(air['机场编码'].values, air['城市名称'].values)
    df['到达城市'] = df['到达机场'].replace(air['机场编码'].values, air['城市名称'].values)
    airline = df[['飞机编号', '出发城市', '到达城市']]
    # print(airline)
    return airline


if __name__ == '__main__':
    airline = air_data()
    linedata=city_data(airline)
    china_map(linedata)




