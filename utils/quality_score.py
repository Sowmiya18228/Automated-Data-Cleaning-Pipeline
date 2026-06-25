def calculate_quality(df):

    total_missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    score = max(
        0,
        100 - (
            (total_missing / max(df.size, 1)) * 50
            +
            (duplicates / max(len(df), 1)) * 50
        )
    )

    return round(score, 2)