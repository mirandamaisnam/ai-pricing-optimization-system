# AI-Powered Pricing Optimization & Revenue Forecasting System

> An end-to-end system that forecasts product demand, estimates price elasticity,
> and recommends revenue-optimizing prices — with explainability, deployment,
> and monitoring built in from day one, not bolted on at the end.

---

## Table of Contents
- [Business Problem](#business-problem)
- [Architecture](#architecture)
- [Dataset Strategy](#dataset-strategy)
- [Tech Stack](#tech-stack)
- [Project Phases](#project-phases)
- [Results](#results)
- [How to Run](#how-to-run)
- [Repository Structure](#repository-structure)

---

## Business Problem

<!-- TODO: 2-3 sentences. Who has this problem, what decision does this system
help them make, and what's the cost of getting it wrong today (e.g., static
pricing leaves revenue on the table, manual pricing doesn't account for
demand elasticity, etc.) -->

---

## Architecture

```
                    BUSINESS PROBLEM
                          │
                          ▼
                   Data Collection
                          │
                          ▼
              SQL Database (PostgreSQL)
                          │
                          ▼
         Data Cleaning ↔ EDA (iterative)
                          │
                          ▼
              Feature Engineering Pipeline
                          │
       ┌──────────────────┴───────────────────┐
       ▼                                       ▼
Demand Forecasting                     Price Elasticity
(Prophet/XGBoost)                    (Statsmodels/EconML)
       │                                       │
       └──────────────────┬────────────────────┘
                          ▼
              MLflow Experiment Tracking
                          │
                          ▼
              Price Optimization Engine
                    (SciPy Optimizer)
                          │
                          ▼
         FastAPI Prediction Service
      (Predictions + SHAP Explanations)
                          │
                          ▼
          Streamlit Business Dashboard
                          │
                          ▼
       Docker → AWS Deployment → Monitoring
                          │
                          ▼
             Drift Detection / Metrics
                          │
                          ▼
                Retraining Trigger ──► loops back to
                                       Feature Engineering
```

---

## Dataset Strategy

This project deliberately uses **two datasets**, each chosen for what it's
actually suited for — rather than forcing one dataset to do a job it wasn't
designed for.

| Dataset | Used for | Why |
|---|---|---|
| [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) | SQL analytics, EDA, dashboarding, demand forecasting, revenue analysis | Real relational transaction data — ideal for SQL joins, business analytics, and time-series demand patterns |
| [Retail Price Optimization](https://www.kaggle.com/datasets/rabieelkharoua/retail-price-optimization) | Price elasticity estimation, price optimization | Olist records transactions, not pricing experiments — most products don't have enough price variation over time to estimate elasticity reliably. This dataset is purpose-built for that. |

<!-- TODO: once you validate the second dataset's price variation, add a short
note here confirming it (e.g., "Products X, Y show 3+ distinct price points
over the observed period, sufficient for log-log elasticity estimation.") -->

These datasets are **not joined** — they power two independent modules within
the same architectural pattern.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Storage | PostgreSQL, DuckDB |
| EDA / Analytics | Pandas, SQL |
| Forecasting | Prophet, XGBoost |
| Elasticity | Statsmodels, EconML |
| Optimization | SciPy |
| Explainability | SHAP |
| Experiment Tracking | MLflow |
| API | FastAPI |
| Dashboard | Streamlit |
| Deployment | Docker, AWS (ECS/Lambda) |
| CI/CD | GitHub Actions |
| Monitoring | CloudWatch / Evidently AI |

---

## Project Phases

Each phase below is documented with its own business objective, technical
objective, and notes — see linked docs/notebooks per phase.

### Phase 0 — Project Setup
<!-- TODO -->

### Phase 1 — Data Collection
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 2 — SQL Analytics
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 3 — Data Cleaning & EDA
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 4 — Feature Engineering
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 5 — Demand Forecasting
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 6 — Price Elasticity
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 7 — Price Optimization
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 8 — Explainability (SHAP)
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 9 — FastAPI Service
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 10 — Streamlit Dashboard
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

### Phase 11 — MLOps (Docker, AWS, Monitoring)
**Business objective:** <!-- TODO -->
**Technical objective:** <!-- TODO -->

---

## Results

<!-- TODO: fill in once you have numbers. Recruiters weight this section
heavily — be specific and quantified. E.g.:
- "Recommended pricing improved projected revenue by X% over static pricing
  on holdout data"
- "Demand forecast MAPE: X% (Prophet) vs Y% (XGBoost baseline)"
- "Estimated price elasticity for top 5 categories: [table]"
-->

---

## How to Run

```bash
# 1. Clone and set up environment
git clone <your-repo-url>
cd pricing-optimization-system
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Set up environment variables
cp .env.example .env            # then fill in your local DB credentials

# 3. Set up PostgreSQL and load data
# <!-- TODO: add exact script/command once Phase 1 is built -->

# 4. Run the API
uvicorn src.api.main:app --reload

# 5. Run the dashboard
streamlit run dashboard/app.py
```

---

## Repository Structure

```
pricing-optimization-system/
├── data/
│   ├── raw/                 # raw datasets (gitignored, sample only)
│   └── processed/           # cleaned/feature-engineered data (gitignored)
├── notebooks/                # EDA, elasticity analysis, model experiments
├── src/
│   ├── data/                  # ingestion, cleaning
│   ├── features/                # feature engineering
│   ├── models/                    # forecasting, elasticity, optimizer
│   ├── api/                         # FastAPI app
│   └── monitoring/                    # drift detection, logging
├── dashboard/                # Streamlit app
├── infra/                     # Dockerfile, AWS deployment config
├── tests/                      # pytest tests
├── .github/workflows/            # CI/CD
├── requirements.txt
├── .env.example
└── README.md
```

---

## Interview Prep Notes

<!-- TODO: as you build each phase, jot down 2-3 interview questions it
prepares you for, and common mistakes you avoided or made. This turns the
repo into a teaching artifact, not just a codebase. -->
