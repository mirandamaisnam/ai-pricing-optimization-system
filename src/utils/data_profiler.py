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

def profile_dataset(df, dataset_name):

    print("=" * 70)
    print(f"Dataset: {dataset_name}")
    print("=" * 70)

    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nMemory Usage:")
    print(f"{df.memory_usage(deep=True).sum()/1024:.2f} KB")

    print("\nFirst Five Rows:")
    print(df.head())