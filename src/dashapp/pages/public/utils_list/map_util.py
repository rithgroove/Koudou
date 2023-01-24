def build_option_list(tsukuba_map):
    return tsukuba_map['type'].unique().tolist()


def count_business_number(filter_list, filer_df):
    dict_result = {}
    for item in filter_list:
        target_len = len(filer_df.loc[filer_df['type'] == item])
        dict_result[item] = target_len
    return dict_result


def build_map_data_table():
    pass
