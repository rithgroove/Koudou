import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px


def table_return_html(counts_dict):
    proportion_list = []
    counts_sum = np.sum(list(counts_dict.values()))
    for value in list(counts_dict.values()):
        proportion_list.append(str(format((value / counts_sum * 100), '.3f')) + '%')
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Location', 'Average Count', 'Proportion'],
                    line_color='darkslategray',
                    fill_color='lightskyblue',
                    align='center'),
        cells=dict(values=[list(counts_dict.keys()),
                           list(counts_dict.values()),
                           proportion_list],
                   line_color='darkslategray',
                   fill_color='lightcyan',
                   align='center'))
    ])
    fig.update_layout(
        height=300,
        showlegend=True,
        margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=0),
    )
    return fig


def pie_return_html(counts_dict):
    counts_pd = pd.DataFrame({
        'location': counts_dict.keys(),
        'counts': counts_dict.values()
    })
    fig = px.pie(counts_pd, names="location", values="counts",
                 # 不同颜色：RdBu、Peach
                 color_discrete_sequence=px.colors.sequential.Peach  # 只需要改变最后的RdBu即可
                 )
    colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', 'cyan']
    fig.update_traces(
        hoverinfo='label+percent',
        textinfo='value',
        textfont_size=10,
        marker=dict(colors=colors,
                    line=dict(color='#000000', width=2)))
    fig.update_layout(
        height=300,
        # width=80,
        showlegend=True,
        margin=go.layout.Margin(l=0, r=0, b=0, t=0, pad=0),  # pad参数是刻度与标签的距离
    )
    return fig