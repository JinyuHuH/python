import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Map  # Map类用于绘制地图
from pyecharts.charts import Pie

world_data = pd.read_excel(r"E:\全球疫情.xlsx")
contry_name = pd.read_excel(r"E:\国家名称中英表.xlsx")
world_data['city'] = world_data['城市'].replace(contry_name['中文'].values ,contry_name['英文'].values)

heatmap_data = world_data[['city','累计确诊']].values.tolist()
#print(heatmap_data)
#热力图
map = Map().add(series_name = "累计确诊人数", # 设置提示框标签
                 data_pair = heatmap_data, # 输入数据
                 maptype = "world", # 设置地图类型为世界地图
                 is_map_symbol_show = False # 不显示标记点
                )
# 设置系列配置项
map.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示国家（标签）名称
# 设置全局配置项
map.set_global_opts(title_opts = opts.TitleOpts(title="世界各国家累计确诊人数地图"), # 设置图标题
                     # 设置视觉映射配置项
                     visualmap_opts = opts.VisualMapOpts(pieces=[ # 自定义分组的分点和颜色
                                                               {"min": 10000,"color":"#800000"}, # 栗色
                                                               {"min": 5000, "max": 9999, "color":"#B22222"}, # 耐火砖
                                                               {"min": 999, "max": 4999,"color":"#CD5C5C"}, # 印度红
                                                               {"min": 100, "max": 999, "color":"#BC8F8F"}, # 玫瑰棕色
                                                               {"max": 99, "color":"#FFE4E1"}, # 薄雾玫瑰
                                                              ],
                     is_piecewise = True))  # 显示分段式图例
map.render('全球疫情热力图.html')
#玫瑰图
death = world_data[['城市','死亡人数']].sort_values(by='死亡人数',ascending=False).values
print(death)
pie = Pie().add("累计死亡人数", # 添加提示框标签
                death, # 输入数据
                radius = ["10%", "80%"],  # 设置内半径和外半径
                center = ["75%", "60%"],  # 设置圆心位置
                rosetype = "radius")   # 玫瑰图模式，通过半径区分数值大小，角度大小表示占比

pie.set_global_opts(title_opts = opts.TitleOpts(title="世界国家累计死亡人数玫瑰图",  # 设置图标题
                                                pos_right = '70%'),  # 图标题的位置
                    legend_opts = opts.LegendOpts( # 设置图例
                                                orient='vertical', # 垂直放置图例
                                                pos_right="40%", # 设置图例位置
                                                pos_top="15%"))

pie.set_series_opts(label_opts = opts.LabelOpts(formatter="{b} : {d}%")) # 设置标签文字形式为（国家：占比（%））
pie.render('全球死亡人数饼图.html')
