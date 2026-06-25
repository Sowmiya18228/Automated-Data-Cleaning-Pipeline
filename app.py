import streamlit as st
import pandas as pd
import plotly.express as px

from utils.profiling import get_summary
from utils.cleaning import handle_missing
from utils.outliers import remove_outliers
from utils.preprocessing import encode_data
from utils.quality_score import calculate_quality

st.set_page_config(
    page_title="Automated Data Cleaning Pipeline",
    layout="wide"
)

st.title("🚀 Automated Data Cleaning and Preprocessing Pipeline")

uploaded_file = st.file_uploader(
    "Upload Dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Load Dataset
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)


    import os

    os.makedirs("data", exist_ok=True)

    df.to_csv(
        "data/uploaded_dataset.csv",
        index=False
    )

    st.success("Dataset Uploaded Successfully!")


    # Dataset Preview
    st.subheader("📄 Dataset Preview (First 5 Rows)")
    st.dataframe(df.head())

    with st.expander("📂 View Complete Dataset"):
        st.dataframe(df)

    # Dataset Summary
    summary = get_summary(df)

    st.subheader("📊 Dataset Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", summary["rows"])
    col2.metric("Columns", summary["columns"])
    col3.metric("Missing Values", summary["missing"])
    col4.metric("Duplicates", summary["duplicates"])

    # Data Types
    st.subheader("Column Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str)
    })

    st.dataframe(dtype_df)

    # Missing Values
    st.subheader("Missing Values Per Column")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Count": df.isnull().sum().values
    })

    st.dataframe(missing_df)

    # Quality Before Cleaning
    quality_before = calculate_quality(df)

    st.subheader("📈 Dataset Quality Before Cleaning")

    st.progress(int(quality_before))
    st.write(f"Quality Score: {quality_before}/100")

    # Cleaning Button
    if st.button("Start Automatic Cleaning"):

        cleaned_df = df.copy()

        # Missing Value Handling
        cleaned_df = handle_missing(cleaned_df)

        # Remove Duplicates
        before_rows = len(cleaned_df)

        cleaned_df.drop_duplicates(inplace=True)

        duplicates_removed = before_rows - len(cleaned_df)

        # Outlier Removal
        numerical_cols = cleaned_df.select_dtypes(
            include='number'
        ).columns

        before_outlier_rows = len(cleaned_df)

        cleaned_df = remove_outliers(
            cleaned_df,
            numerical_cols
        )

        outliers_removed = (
            before_outlier_rows - len(cleaned_df)
        )

        # Encoding
        cleaned_df = encode_data(cleaned_df)

        # Quality After Cleaning
        quality_after = calculate_quality(cleaned_df)

        remaining_missing = (
            cleaned_df.isnull().sum().sum()
        )



        os.makedirs(
            "reports",
            exist_ok=True
        )

        report = pd.DataFrame({
            "Metric": [
                "Rows",
                "Missing Before",
                "Missing After",
                "Quality Before",
                "Quality After"
            ],
            "Value": [
                len(df),
                summary["missing"],
                remaining_missing,
                quality_before,
                quality_after
            ]
        })

        report.to_csv(
            "reports/cleaning_report.csv",
            index=False
        )

        # Report
        st.subheader("✅ Cleaning Report")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Duplicates Removed",
            duplicates_removed
        )

        c2.metric(
            "Outliers Removed",
            outliers_removed
        )

        c3.metric(
            "Remaining Missing Values",
            remaining_missing
        )

        # Quality After
        st.subheader("📈 Dataset Quality After Cleaning")

        st.progress(int(quality_after))
        st.write(f"Quality Score: {quality_after}/100")

        # Cleaned Dataset
        st.subheader("🧹 Cleaned Dataset Preview (First 5 Rows)")
        st.dataframe(cleaned_df.head())

        with st.expander("📂 View Complete Cleaned Dataset"):
            st.dataframe(cleaned_df)


        os.makedirs("cleaned_data", exist_ok=True)



        # ==========================
        # VISUALIZATION
        # ==========================

        st.subheader("📊 Missing Values Comparison")

        comparison = pd.DataFrame({
            "Stage": ["Before Cleaning", "After Cleaning"],
            "Missing Values": [
                summary["missing"],
                remaining_missing
            ]
        })

        # Show values in table
        st.dataframe(comparison)

        # Create bar chart
        fig = px.bar(
            comparison,
            x="Stage",
            y="Missing Values",
            text="Missing Values",
            title="Missing Values Before vs After Cleaning"
        )

        fig.update_traces(textposition="outside")

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        st.subheader("📋 Before vs After Summary")

        comparison_df = pd.DataFrame({
            "Metric": [
                "Rows",
                "Missing Values",
                "Duplicates",
                "Quality Score"
            ],
            "Before": [
                len(df),
                summary["missing"],
                summary["duplicates"],
                quality_before
            ],
            "After": [
                len(cleaned_df),
                remaining_missing,
                cleaned_df.duplicated().sum(),
                quality_after
            ]
        })

        st.dataframe(comparison_df)
        # ==========================
        # QUALITY SCORE COMPARISON
        # ==========================

        st.subheader("📈 Quality Score Comparison")

        quality_df = pd.DataFrame({
            "Stage": ["Before Cleaning", "After Cleaning"],
            "Quality Score": [
                quality_before,
                quality_after
            ]
        })

        st.dataframe(quality_df)

        quality_fig = px.bar(
            quality_df,
            x="Stage",
            y="Quality Score",
            text="Quality Score",
            title="Dataset Quality Score Improvement"
        )

        quality_fig.update_traces(textposition="outside")

        st.plotly_chart(
            quality_fig,
            use_container_width=True
        )



        os.makedirs(
            "cleaned_data",
            exist_ok=True
        )

        cleaned_df.to_csv(
            "cleaned_data/cleaned_dataset.csv",
            index=False
        )


        # Download Dataset
        csv = cleaned_df.to_csv(index=False)

        st.download_button(
            label="⬇ Download Cleaned Dataset",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )