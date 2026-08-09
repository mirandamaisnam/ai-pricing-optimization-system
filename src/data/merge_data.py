import pandas as pd


def validate_merge(before_rows, after_rows, merge_name):
    """
    Validate whether a merge changed the number of rows.
    """

    print(f"\n{'=' * 60}")
    print(merge_name)
    print("=" * 60)

    print(f"Rows before merge : {before_rows:,}")
    print(f"Rows after merge  : {after_rows:,}")

    if before_rows == after_rows:
        print(" Row count preserved.")
    elif after_rows > before_rows:
        print(" Row count increased.")
    else:
        print(" Row count decreased.")


def merge_orders_customers(orders_df, customers_df):
    """
    Merge Orders with Customers.
    """

    before_rows = len(orders_df)

    merged_df = pd.merge(
        orders_df,
        customers_df,
        on="customer_id",
        how="left"
    )

    after_rows = len(merged_df)

    validate_merge(
        before_rows,
        after_rows,
        "Orders + Customers"
    )

    return merged_df
def merge_order_items(master_df, order_items_df):

    before_rows = len(master_df)

    merged_df = pd.merge(
        master_df,
        order_items_df,
        on="order_id",
        how="inner"
    )

    after_rows = len(merged_df)

    print("=" * 60)
    print("Master + Order Items")
    print("=" * 60)
    print(f"Rows before merge : {before_rows:,}")
    print(f"Rows after merge  : {after_rows:,}")

    if after_rows > before_rows:
        print("Row count increased.")
    elif after_rows < before_rows:
        print("Row count decreased.")
    else:
        print("Row count preserved.")

    return merged_df
def merge_products(master_df, products_df):

    before_rows = len(master_df)

    merged_df = pd.merge(
        master_df,
        products_df,
        on="product_id",
        how="left"
    )

    after_rows = len(merged_df)

    validate_merge(
        before_rows,
        after_rows,
        "Master + Products"
    )

    return merged_df
def merge_payments(master_df, payments_df):
    """
    Aggregate payment records to one row per order
    and merge them into the master analytical dataset.

    Final grain remains:
    one row = one order item.
    """

    payment_summary = (
        payments_df
        .groupby("order_id")
        .agg(
            total_payment_value=("payment_value", "sum"),
            payment_count=("payment_sequential", "count"),
            max_installments=("payment_installments", "max")
        )
        .reset_index()
    )

    before_rows = len(master_df)

    merged_df = pd.merge(
        master_df,
        payment_summary,
        on="order_id",
        how="left"
    )

    after_rows = len(merged_df)

    validate_merge(
        before_rows,
        after_rows,
        "Master + Payments"
    )

    return merged_df