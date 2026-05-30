import duckdb
import os

# ── Connect to a persistent DuckDB database file ──────────────────────────────
con = duckdb.connect("output/superstore.duckdb")

# ── Run the SQL model file ────────────────────────────────────────────────────
with open("sql/model.sql", "r") as f:
    sql = f.read()

con.execute(sql)
print("✓ Views created successfully")

# ── Verify each view ──────────────────────────────────────────────────────────
views = [
    "kpi_summary",
    "kpi_monthly_trend",
    "kpi_regional",
    "kpi_category",
    "kpi_seasonality_gap",
]

for view in views:
    result = con.execute(f"SELECT * FROM {view} LIMIT 3").df()
    print(f"\n── {view} ──")
    print(result.to_string())

# ── Export each KPI view to CSV (for Power BI import) ─────────────────────────
os.makedirs("output/kpis", exist_ok=True)

for view in views:
    df = con.execute(f"SELECT * FROM {view}").df()
    path = f"output/kpis/{view}.csv"
    df.to_csv(path, index=False)
    print(f"✓ Exported {view} → {path}")

con.close()
print("\n✓ DuckDB model complete")
