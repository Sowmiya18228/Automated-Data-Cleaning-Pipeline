def get_summary(df):

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing": df.isnull().sum().sum(),
        "duplicates": df.duplicated().sum()
    }