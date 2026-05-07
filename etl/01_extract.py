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