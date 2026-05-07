""" 
    This script extracts data from the SQLite database 
    and saves it as CSV files to the staging directory
    (data/staging/). This is the first step in the ETL 
    process, where we move the raw data into a format 
    that can be easily transformed.

    Source:     data/raw/database.sqlite (Kaggle European Soccer Database)
    Output:     data/staging/*.csv

    Tables Extracted:
        - Match:    data/staging/match.csv
        - Team:     data/staging/team.csv
        - Player:   data/staging/player.csv
        - League:   data/staging/league.csv
        - Country:  data/staging/country.csv
    
    Usage:
    python3 etl/01_extract.py

    Dependencies:
        - sqlite3
        - pandas
"""

import sqlite3
import pandas as pd
import os

# Connect to SQLite
connection = sqlite3.connect("data/raw/database.sqlite")

# Extract each table 
print("Extracting tables from SQLite...")

df_match = pd.read_sql("SELECT * FROM Match", connection)
df_team = pd.read_sql("SELECT * FROM Team", connection)
df_player = pd.read_sql("SELECT * FROM Player", connection)
df_league = pd.read_sql("SELECT * FROM League", connection)
df_country = pd.read_sql("SELECT * FROM Country", connection)

connection.close()

# Save to staging as CSVs
os.makedirs("data/staging", exist_ok=True)

df_match.to_csv("data/staging/match.csv", index=False)
df_team.to_csv("data/staging/team.csv", index=False)
df_player.to_csv("data/staging/player.csv", index=False)
df_league.to_csv("data/staging/league.csv", index=False)
df_country.to_csv("data/staging/country.csv", index=False)

print("Extraction complete. Files saved to data/staging/")
print(f"    Match rows:     {len(df_match)}")
print(f"    Team rows:      {len(df_team)}")
print(f"    Player rows:    {len(df_player)}")
print(f"    League rows:    {len(df_league)}")
print(f"    Country rows:   {len(df_country)}")