import numpy as np

def location_divider(df_agent_position_summary):
    list_locations = []
    unique_location_list = df_agent_position_summary['location'].unique()

    for location in unique_location_list:
        this_location_list = df_agent_position_summary.loc[df_agent_position_summary['location'] == location]
        list_locations.append(this_location_list)

    df_comp = location_df_processor(list_locations)
    return df_comp


def location_df_processor(position_list):
    init_df = position_list[0]
    init_df.drop(['location'], axis=1)
    init_df.rename(columns={'count': 'home'})
    for df in position_list:
        pass
    return position_list


def proportion_calculation(df):
    result_dict = {}
    timestamp_length = int(df.loc[len(df) - 1, 'time_stamp']) / 5
    unique_location_list = df['location'].unique()
    for location in unique_location_list:
        single_location_df = df.loc[df['location'] == location]
        mean_count = np.sum(single_location_df['count']) / timestamp_length
        result_dict[location] = round(mean_count, 2)

    return result_dict