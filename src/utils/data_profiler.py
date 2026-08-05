import pandas as pd


def profile_summary(datasets):

    summary = []

    for dataset_name, df in datasets.items():

        total_cells = df.shape[0] * df.shape[1]

        missing_values = df.isnull().sum().sum()

        duplicate_rows = df.duplicated().sum()

        object_cols = df.select_dtypes(include="object").shape[1]

        numeric_cols = df.select_dtypes(include=["int64", "float64"]).shape[1]

        summary.append({
            "Dataset": dataset_name,
            "Rows": df.shape[0],
            "Columns": df.shape[1],
            "Missing Values": missing_values,
            "Missing %": round((missing_values / total_cells) * 100, 2),
            "Duplicate Rows": duplicate_rows,
            "Duplicate %": round((duplicate_rows / df.shape[0]) * 100, 2),
            "Object Columns": object_cols,
            "Numeric Columns": numeric_cols,
            "Memory (KB)": round(df.memory_usage(deep=True).sum() / 1024, 2)
        })

    return pd.DataFrame(summary)


def missing_value_report(df):

    missing_count = df.isnull().sum()

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": missing_count.values,
        "Missing %": ((missing_count / len(df)) * 100).round(2).values,
        "Data Type": df.dtypes.values
    })

    missing = missing.sort_values(
        by="Missing Values",
        ascending=False
    )

    return missing