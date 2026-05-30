import pandas as pd
import os

# ── 1. Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv("data/Sample - Superstore.csv", encoding="latin-1")
print(f"Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ── 2. Standardize column names ───────────────────────────────────────────────
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)
print("Columns renamed:", df.columns.tolist())

# ── 3. Parse dates ────────────────────────────────────────────────────────────
df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y")
df["ship_date"]  = pd.to_datetime(df["ship_date"],  format="%m/%d/%Y")

# ── 4. Drop duplicates ────────────────────────────────────────────────────────
before = len(df)
df = df.drop_duplicates(subset="order_id", keep="first")
print(f"Duplicates removed: {before - len(df)}")

# ── 5. Drop nulls in critical columns ─────────────────────────────────────────
df = df.dropna(subset=["sales", "profit", "quantity", "order_date"])
print(f"Rows after null drop: {len(df)}")

# ── 6. Fix data types ─────────────────────────────────────────────────────────
df["sales"]    = df["sales"].astype(float).round(2)
df["profit"]   = df["profit"].astype(float).round(2)
df["discount"] = df["discount"].astype(float).round(2)
df["quantity"] = df["quantity"].astype(int)

# ── 7. Feature engineering ────────────────────────────────────────────────────
df["profit_margin"]  = (df["profit"] / df["sales"]).round(4)
df["order_year"]     = df["order_date"].dt.year
df["order_month"]    = df["order_date"].dt.month
df["order_quarter"]  = df["order_date"].dt.quarter
df["ship_days"]      = (df["ship_date"] - df["order_date"]).dt.days

# Month name for readable charts later
df["month_name"] = df["order_date"].dt.strftime("%b")

# Season column (useful for seasonality gap analysis)
def get_season(month):
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"

df["season"] = df["order_month"].apply(get_season)

# ── 8. Validation prints ──────────────────────────────────────────────────────
print("\n── Sample rows ──")
print(df.head(3).to_string())

print("\n── Profit margin range ──")
print(df["profit_margin"].describe())

print("\n── Sales by region ──")
print(df.groupby("region")["sales"].sum().round(2))

print("\n── Orders by season ──")
print(df.groupby("season")["sales"].sum().round(2).sort_values(ascending=False))

# ── 9. Export clean CSV ───────────────────────────────────────────────────────
os.makedirs("output", exist_ok=True)
df.to_csv("output/superstore_clean.csv", index=False)
print(f"\n✓ Clean file saved → output/superstore_clean.csv ({len(df)} rows)")
