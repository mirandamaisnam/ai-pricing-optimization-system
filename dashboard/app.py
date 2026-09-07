import streamlit as st
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Pricing Optimization System",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed"

master_df = pd.read_csv(
    DATA_PATH / "master_dataset.csv"
)

elasticity_df = pd.read_csv(
    DATA_PATH / "price_elasticity_results.csv"
)

optimization_df = pd.read_csv(
    DATA_PATH / "price_optimization_results.csv"
)

forecast_df = pd.read_csv(
    DATA_PATH / "demand_forecast_results.csv"
)

master_df["order_purchase_timestamp"] = pd.to_datetime(
    master_df["order_purchase_timestamp"],
    errors="coerce"
)

forecast_df["date"] = pd.to_datetime(
    forecast_df["date"],
    errors="coerce"
)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def format_category(category):
    return category.replace("_", " ").title()


def format_currency(value):
    if value >= 1_000_000:
        return f"R$ {value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"R$ {value / 1_000:.1f}K"
    else:
        return f"R$ {value:,.0f}"


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("Dashboard")

st.sidebar.markdown(
    "Use the controls below to explore the pricing analysis."
)

categories = sorted(
    master_df["product_category_name"]
    .dropna()
    .unique()
)

category_options = ["All Categories"] + categories

selected_category = st.sidebar.selectbox(
    "Product Category",
    category_options,
    format_func=lambda x: (
        x if x == "All Categories"
        else format_category(x)
    )
)

st.sidebar.divider()

st.sidebar.markdown("### Project Scope")

st.sidebar.caption(
    "Brazilian e-commerce pricing analysis using "
    "demand forecasting, price elasticity, and "
    "scenario-based optimization."
)

st.sidebar.markdown("### Data")

st.sidebar.caption(
    f"{len(master_df):,} order items"
)

st.sidebar.caption(
    f"{master_df['product_category_name'].nunique():,} categories"
)


# --------------------------------------------------
# Apply category filter
# --------------------------------------------------

filtered_df = master_df.copy()

if selected_category != "All Categories":
    filtered_df = filtered_df[
        filtered_df["product_category_name"] == selected_category
    ]


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("AI-Powered Pricing Optimization System")

st.markdown(
    """
    **Demand Forecasting • Price Elasticity • Revenue Optimization**

    An interactive analytics dashboard built from the Olist Brazilian
    e-commerce dataset to analyze demand, pricing behavior, and
    scenario-based price recommendations.
    """
)


st.divider()


# ==================================================
# TABS
# ==================================================

overview_tab, forecast_tab, elasticity_tab, optimization_tab = st.tabs(
    [
        "Overview",
        "Demand Forecast",
        "Price Elasticity",
        "Price Optimization"
    ]
)


# ==================================================
# OVERVIEW
# ==================================================

with overview_tab:

    st.subheader("Business Overview")

    # --------------------------------------------------
    # KPI calculations
    # --------------------------------------------------

    total_revenue = filtered_df["price"].sum()
    units_sold = len(filtered_df)
    average_price = filtered_df["price"].mean()
    category_count = filtered_df["product_category_name"].nunique()

    # --------------------------------------------------
    # KPI cards
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Revenue",
            format_currency(total_revenue)
        )

    with col2:
        st.metric(
            "Units Sold",
            f"{units_sold:,}"
        )

    with col3:
        st.metric(
            "Average Price",
            f"R$ {average_price:,.2f}"
        )

    with col4:
        st.metric(
            "Categories",
            f"{category_count:,}"
        )

    st.divider()

    # --------------------------------------------------
    # Revenue Trend
    # --------------------------------------------------

    st.subheader("Revenue Trend")

    daily_revenue = (
        filtered_df
        .dropna(subset=["order_purchase_timestamp"])
        .assign(
            date=lambda x: x["order_purchase_timestamp"].dt.date
        )
        .groupby("date")["price"]
        .sum()
    )

    st.line_chart(daily_revenue)

    # --------------------------------------------------
    # Revenue by Category
    # --------------------------------------------------

    st.subheader("Revenue by Product Category")

    category_revenue = (
        filtered_df
        .groupby("product_category_name")["price"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
    )

    category_revenue.index = [
        format_category(category)
        for category in category_revenue.index
    ]

    st.bar_chart(category_revenue)


# ==================================================
# DEMAND FORECAST
# ==================================================

with forecast_tab:

    st.subheader("Demand Forecast")

    st.markdown(
        """
        The chart compares actual demand with model predictions
        over the 30-day holdout period used in the forecasting analysis.
        """
    )

    # --------------------------------------------------
    # Selected model
    # --------------------------------------------------

    selected_model = forecast_df["selected_model"].iloc[0]

    st.write(
        f"**Selected forecasting model:** {selected_model.title()}"
    )

    # --------------------------------------------------
    # Forecast chart
    # --------------------------------------------------

    forecast_chart = (
        forecast_df[
            ["date", "actual_demand", "forecast"]
        ]
        .dropna()
        .sort_values("date")
        .set_index("date")
    )

    st.line_chart(forecast_chart)

    # --------------------------------------------------
    # Forecast summary
    # --------------------------------------------------

    actual_total = forecast_df["actual_demand"].sum()
    forecast_total = forecast_df["forecast"].sum()

    if actual_total != 0:
        forecast_difference_pct = (
            (forecast_total - actual_total)
            / actual_total
        ) * 100
    else:
        forecast_difference_pct = 0

    forecast_col1, forecast_col2, forecast_col3 = st.columns(3)

    with forecast_col1:
        st.metric(
            "Actual Demand",
            f"{actual_total:,.0f}"
        )

    with forecast_col2:
        st.metric(
            "Forecasted Demand",
            f"{forecast_total:,.0f}"
        )

    with forecast_col3:
        st.metric(
            "Forecast Difference",
            f"{forecast_difference_pct:+.1f}%"
        )

    # --------------------------------------------------
    # Forecast Performance
    # --------------------------------------------------

    st.markdown("#### Forecast Performance")

    actual = forecast_df["actual_demand"]
    predicted = forecast_df["forecast"]

    mae = (actual - predicted).abs().mean()

    rmse = (
        ((actual - predicted) ** 2).mean()
    ) ** 0.5

    if actual.abs().sum() != 0:
        wape = (
            (actual - predicted).abs().sum()
            / actual.abs().sum()
        ) * 100
    else:
        wape = 0

    smape_denominator = (
        actual.abs() + predicted.abs()
    )

    valid_smape = smape_denominator != 0

    if valid_smape.any():
        smape = (
            2
            * (actual[valid_smape] - predicted[valid_smape]).abs()
            / smape_denominator[valid_smape]
        ).mean() * 100
    else:
        smape = 0

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric(
            "MAE",
            f"{mae:.2f}"
        )

    with metric_col2:
        st.metric(
            "RMSE",
            f"{rmse:.2f}"
        )

    with metric_col3:
        st.metric(
            "WAPE",
            f"{wape:.1f}%"
        )

    with metric_col4:
        st.metric(
            "sMAPE",
            f"{smape:.1f}%"
        )

    st.caption(
        "Forecast results are evaluated on the held-out period. "
        "The forecast is intended for demand planning and scenario analysis."
    )


# ==================================================
# PRICE ELASTICITY
# ==================================================

with elasticity_tab:

    st.subheader("Price Elasticity Analysis")

    st.markdown(
        """
        Price elasticity measures how demand responds to changes in price.
        More negative values indicate greater price sensitivity.
        """
    )

    # --------------------------------------------------
    # Category selector
    # --------------------------------------------------

    elasticity_categories = sorted(
        elasticity_df[
            ~elasticity_df["category"].str.startswith("__")
        ]["category"]
        .dropna()
        .unique()
    )

    selected_elasticity_category = st.selectbox(
        "Select a category for elasticity analysis",
        elasticity_categories,
        format_func=format_category
    )

    selected_elasticity = elasticity_df[
        elasticity_df["category"] == selected_elasticity_category
    ].iloc[0]

    # --------------------------------------------------
    # Elasticity KPIs
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Elasticity",
            f"{selected_elasticity['elasticity']:.2f}"
        )

    with col2:
        st.metric(
            "Average Price",
            f"R$ {selected_elasticity['average_price']:.2f}"
        )

    with col3:
        st.metric(
            "Reliability",
            selected_elasticity["reliability_flag"]
            .replace("_", " ")
            .title()
        )

    st.write(
        f"**95% Confidence Interval:** "
        f"{selected_elasticity['ci_low']:.2f} "
        f"to "
        f"{selected_elasticity['ci_high']:.2f}"
    )

    # --------------------------------------------------
    # Category comparison
    # --------------------------------------------------

    st.markdown("#### Category Elasticity Comparison")

    category_elasticity = elasticity_df[
        ~elasticity_df["category"].str.startswith("__")
    ].copy()

    category_elasticity = category_elasticity[
        category_elasticity["elasticity"].notna()
    ]

    elasticity_chart = (
        category_elasticity[
            ["category", "elasticity"]
        ]
        .sort_values("elasticity")
        .set_index("category")
    )

    elasticity_chart.index = [
        format_category(category)
        for category in elasticity_chart.index
    ]

    st.bar_chart(elasticity_chart)

    # --------------------------------------------------
    # Model details
    # --------------------------------------------------

    st.markdown("#### Model Details")

    detail_col1, detail_col2, detail_col3 = st.columns(3)

    with detail_col1:
        st.metric(
            "Observations",
            f"{int(selected_elasticity['n_obs']):,}"
        )

    with detail_col2:
        st.metric(
            "Products",
            f"{int(selected_elasticity['n_products']):,}"
        )

    with detail_col3:
        st.metric(
            "Within R²",
            f"{selected_elasticity['r2_within']:.3f}"
        )

    st.caption(
        "Elasticity estimates are observational and should be interpreted "
        "as scenario-based decision support rather than causal price effects."
    )


# ==================================================
# PRICE OPTIMIZATION
# ==================================================

with optimization_tab:

    st.subheader("Price Optimization")

    st.markdown(
        """
        Explore category-level pricing scenarios based on the estimated
        price elasticity. The recommendation is evaluated within the
        model's candidate price range and should be treated as
        scenario-based decision support.
        """
    )

    # --------------------------------------------------
    # Category selector
    # --------------------------------------------------

    optimization_categories = sorted(
        optimization_df[
            optimization_df["recommendation_flag"] != "not_recommended"
        ]["category"]
        .dropna()
        .unique()
    )

    selected_optimization_category = st.selectbox(
        "Select a category for price optimization",
        optimization_categories,
        format_func=format_category
    )

    selected_optimization = optimization_df[
        optimization_df["category"] == selected_optimization_category
    ].iloc[0]

    # --------------------------------------------------
    # Optimization KPIs
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Reference Price",
            f"R$ {selected_optimization['reference_price']:.2f}"
        )

    with col2:
        st.metric(
            "Scenario Price",
            f"R$ {selected_optimization['recommended_price']:.2f}"
        )

    with col3:
        st.metric(
            "Expected Revenue",
            f"R$ {selected_optimization['expected_revenue']:,.2f}"
        )

    with col4:
        st.metric(
            "Revenue Change",
            f"{selected_optimization['revenue_change_pct']:.1f}%"
        )

    # --------------------------------------------------
    # Pricing scenario
    # --------------------------------------------------

    st.markdown("#### Pricing Scenario")

    scenario_col1, scenario_col2, scenario_col3 = st.columns(3)

    with scenario_col1:
        st.metric(
            "Price Change",
            f"{selected_optimization['price_change_pct']:.1f}%"
        )

    with scenario_col2:
        st.metric(
            "Baseline Demand",
            f"{selected_optimization['baseline_demand']:.2f}"
        )

    with scenario_col3:
        st.metric(
            "Expected Demand",
            f"{selected_optimization['expected_demand']:.2f}"
        )

    # --------------------------------------------------
    # Revenue comparison
    # --------------------------------------------------

    st.markdown("#### Baseline vs Scenario Revenue")

    revenue_comparison = pd.DataFrame(
        {
            "Revenue": [
                selected_optimization["baseline_revenue"],
                selected_optimization["expected_revenue"]
            ]
        },
        index=[
            "Baseline",
            "Scenario"
        ]
    )

    st.bar_chart(revenue_comparison)

    # --------------------------------------------------
    # Recommendation details
    # --------------------------------------------------

    st.markdown("#### Recommendation Details")

    detail_col1, detail_col2, detail_col3 = st.columns(3)

    with detail_col1:
        st.write(
            "**Recommendation:**",
            selected_optimization["recommendation_flag"]
            .replace("_", " ")
            .title()
        )

    with detail_col2:
        st.write(
            "**Elasticity:**",
            f"{selected_optimization['elasticity']:.2f}"
        )

    with detail_col3:
        extrapolation_status = (
            "Yes"
            if bool(selected_optimization["extrapolation_flag"])
            else "No"
        )

        st.write(
            "**Outside observed price range:**",
            extrapolation_status
        )

    st.caption(
        "The optimization uses a constant-elasticity revenue scenario "
        "within the candidate price grid. It does not represent a "
        "causal guarantee of future revenue."
    )
    # ==================================================
# ABOUT THE ANALYSIS
# ==================================================

st.divider()

st.subheader("About This Analysis")

about_col1, about_col2 = st.columns(2)

with about_col1:
    st.markdown(
        """
        **Objective**

        This system analyzes historical Olist e-commerce data to
        support pricing decisions through three analytical stages:

        - Demand forecasting
        - Price elasticity estimation
        - Scenario-based price optimization
        """
    )

with about_col2:
    st.markdown(
        """
        **Methodology**

        Demand is forecast using time-series and machine-learning
        approaches. Price elasticity is estimated using product and
        time fixed effects. Pricing scenarios then use the estimated
        elasticity to evaluate expected demand and revenue under
        alternative prices.
        """
    )

st.caption(
    "The analysis is based on observational e-commerce data. "
    "Pricing recommendations are scenario-based and should not be "
    "interpreted as causal guarantees."
)