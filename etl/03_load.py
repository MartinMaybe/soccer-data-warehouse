import pandas as pd
from sqlalchemy import create_engine

# Connection 
print("Connecting to PostgreSQL...")
engine = create_engine("postgresql+psycopg2://martin@localhost:5432/soccer_dw")

# List tables (dimensions first)
tables = [
    ("dim_country", "data/warehouse/dim_country.csv"),
    ("dim_league", "data/warehouse/dim_league.csv"),
    ("dim_team", "data/warehouse/dim_team.csv"),
    ("dim_player", "data/warehouse/dim_player.csv"),
    ("dim_date", "data/warehouse/dim_date.csv"),
    ("fact_match", "data/warehouse/fact_match.csv"),
]

# Load each table
for table_name, file_path in tables:
    print(f"Loading {table_name}...")
    df = pd.read_csv(file_path)
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False
    )
    print(f"    {len(df)} rows loaded into {table_name}")

print("Load Complete!")