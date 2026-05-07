"""
    This script loads the transformed data from the CSV files 
    into the PostgreSQL data warehouse. It uses SQLAlchemy to 
    connect to the database and pandas to read the CSV files and 
    insert them into the corresponding tables. The script processes 
    dimension tables first, followed by the fact table, ensuring 
    referential integrity is maintained.

    Input:      data/warehouse/*.csv
    Output:     PostgreSQL soccer_dw database

    Prerequisites:
        - PostgreSQL running on localhost:5432
        - soccer_dw database created
        - DDL scripts executed (sql/01_create_dimensions.sql,
          sql/02_create_facts.sql)
        - Tables empty (TRUNCATE before re-running)

    Usage:
        python3 etl/03_load.py

    Dependencies:
        - pandas
        - sqlalchemy
        - psycopg2-binary

"""
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