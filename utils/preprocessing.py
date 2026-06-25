from sklearn.preprocessing import LabelEncoder

def encode_data(df):

    encoder = LabelEncoder()

    categorical_cols = df.select_dtypes(
        include=['object']
    ).columns

    for col in categorical_cols:

        try:
            df[col] = encoder.fit_transform(
                df[col].astype(str)
            )

        except Exception:
            pass

    return df