def table_generator(target_dataframe):
    column_list = []
    for item in target_dataframe.columns:
        column_list.append(target_dataframe[item])
    fig = go.Figure(
        data=[go.Table(
            header=dict(values=list(target_dataframe.columns),  # 表头取值是data列属性
                        fill_color='paleturquoise',  # 填充色和文本位置
                        align='left'),
            cells=dict(values=column_list,  # 单元格的取值就是每个列属性的Series取值
                       fill_color='lavender',
                       align='left'
                       )
        )]
    )
    return fig


def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open
