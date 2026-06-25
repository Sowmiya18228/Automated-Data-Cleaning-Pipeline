import numpy as np

def handle_missing(df):

    numerical_cols = df.select_dtypes(
        include=np.number
    ).columns

    categorical_cols = df.select_dtypes(
        exclude=np.number
    ).columns

    for col in numerical_cols:
        df[col] = df[col].fillna(
            df[col].median()
        )

    for col in categorical_cols:

        if df[col].isnull().sum() > 0:

            mode_value = df[col].mode()

            if not mode_value.empty:
                df[col] = df[col].fillna(
                    mode_value[0]
                )

    return df