def ensure_unique_index(data_df):
    return data_df[~data_df.index.duplicated(keep='first')]

def ensure_sorted(data_df):
    return data_df.sort_index()
