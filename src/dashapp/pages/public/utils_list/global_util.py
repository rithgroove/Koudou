from src.util.time_stamp import TimeStamp

def timestamp_converter(timestamp):
    ts = TimeStamp(timestamp)
    time = '[' + str(ts.get_week()) + ' week ' + str(ts.get_day_of_week()) + ' days ' + str(ts.get_hour_min_str()) \
           + ':' + str(ts.get_second()) + ']'
    return time


def df_timestamp_converter(df):
    df.index = range(len(df))
    for i in range(len(df)):
        df.loc[i, 'time_stamp'] = timestamp_converter(df.loc[i, 'time_stamp'])
    return df

def preprocess_linear_data(df):
    temp_list = []
    for i in range(0, len(df), 10):
        temp_list.append(i)
    new_df = df.iloc[temp_list]
    new_df.index = range(len(new_df))
    return new_df