import pandas as pd
from pygments.lexers import go

data=pd.read_csv('E:\Wuhan-2019-nCoV.csv')
date=data['date']
dt_china=data.query("country=='中国'")
dt_oversea=data.query("country!='中国'")
C_confirmed=dt_china['confirmed'].count()
O_confirmed = dt_oversea['confirmed'].count()
y_max = max(C_confirmed,O_confirmed)
# China
trace1 = go.Scatter(x=dt_china.index[:2],
                    y=dt_china['confirmed'][:2],
                    mode='lines',
                    name='China',
                    line=dict(width=1.5,
                              color='#FFD300'))
# oversea
trace2 = go.Scatter(x = dt_oversea.index[:2],
                    y = dt_oversea['confirmed'][:2],
                    mode='lines', # markers+lines
                    name='Oversea',
                    line=dict(width=1.5))
frames = [dict(data= [dict(type='scatter',
                           x=dt_china.index[:k+1],
                           y=dt_china['confirmed'][:k+1]),
                      dict(type='scatter',
                           x=dt_oversea.index[:k+1],
                           y=dt_oversea['confirmed'][:k+1])],
               traces= [0, 1],
               # 0: frames[k]['data'][0]，代表 trace1, 1：frames[k]['data'][1], trace2
              )for k  in  range(1, len(dt_china))]
layout = go.Layout(width=500,
                   height=600,
                   showlegend=True,
                   template='plotly_dark',
                   hovermode='closest',
                   updatemenus=[dict(type='buttons', showactive=False,
                                y=1.10,
                                x=1.15,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None,
                                                    dict(frame=dict(duration=100,
                                                                    redraw=False),
                                                         transition=dict(duration=1),
                                                         fromcurrent=True,
                                                         mode='immediate')])])],
                  )
layout.update(xaxis =dict(range=[dt_china.index[0],
                                 dt_china.index[len(dt_china)-1]+pd.Timedelta(days=2)
                                ],
                          autorange=False),
              yaxis =dict(range=[0, y_max*1.05], autorange=False))
fig = go.Figure(data=[trace1, trace2], frames=frames, layout=layout)
fig.show()
