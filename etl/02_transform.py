"""
    This script performs the transformation step of the ETL process 
    for the soccer dataset. It reads the staged CSV files, transforms 
    them into dimensional tables and a fact table (fact_match), and 
    saves the transformed data back to CSV files in the warehouse folder.

    Input:      data/staging/*.csv
    Output:     data/warehouse/*.csv

    Tables Produced:
        - dim_country   → data/warehouse/dim_country.csv
        - dim_league    → data/warehouse/dim_league.csv
        - dim_team      → data/warehouse/dim_team.csv
        - dim_player    → data/warehouse/dim_player.csv
        - dim_date      → data/warehouse/dim_date.csv
        - fact_match    → data/warehouse/fact_match.csv

    Usage:
        python3 etl/02_transform.py

    Dependencies:
        - pandas
        - lxml
"""
import pandas as pd
import os
from lxml import etree

print("Loading staged data...")

df_match    = pd.read_csv("data/staging/match.csv")
df_team     = pd.read_csv("data/staging/team.csv")
df_player   = pd.read_csv("data/staging/player.csv")
df_league   = pd.read_csv("data/staging/league.csv")
df_country  = pd.read_csv("data/staging/country.csv")

# dim_country
print("Transforming dim_country...")
dim_country = df_country[["id", "name"]].copy()
dim_country.columns = ["country_id", "country_name"]
dim_country = dim_country.dropna(subset=["country_id", "country_name"])

# dim_league
print("Transforming dim_league...")
dim_league = df_league[["id", "country_id", "name"]].copy()
dim_league.columns = ["league_id", "country_id", "league_name"]
dim_league = dim_league.dropna(subset=["league_id", "league_name"])

# dim_team
print("Transforming dim_team...")
dim_team = df_team[["team_api_id", "team_fifa_api_id", "team_long_name", "team_short_name"]].copy()
dim_team = dim_team.dropna(subset=["team_api_id", "team_long_name"])

# dim_player
print("Transforming dim_player...")
dim_player = df_player[["player_api_id", "player_name", "player_fifa_api_id", "birthday", "height", "weight"]].copy()
dim_player = dim_player.dropna(subset=["player_api_id", "player_name"])

# dim_date
print("Transforming dim_date...")
df_match["date"] = pd.to_datetime(df_match["date"])

dim_date = pd.DataFrame() # New empty DataFrame
dim_date["match_date"]  = df_match["date"].dt.date  # Extract specifc pieces
dim_date["year"]        = df_match["date"].dt.year
dim_date["month"]       = df_match["date"].dt.month
dim_date["month_name"]  = df_match["date"].dt.strftime("%B")
dim_date["quarter"]     = df_match["date"].dt.quarter
dim_date["day"]         = df_match["date"].dt.day
dim_date["day_of_week"] = df_match["date"].dt.strftime("%A")
dim_date["season"]      = df_match["season"]

dim_date = dim_date.drop_duplicates(subset=["match_date"]) # removes dupes
dim_date = dim_date.reset_index(drop=True) # resets to fill gaps from removed dupes
dim_date.insert(0, "date_id", dim_date["match_date"].astype(str).str.replace("-", "").astype(int)) # 2008-08-17 --> 20080817 as primary key

# Handle xml from stats (shoton, shotoff, etc)
def parse_xml_count(xml_string, tag):
    """Extract count of events from XML string"""
    try:
        if pd.isna(xml_string) or not str(xml_string).strip().startswith("<"):
            return None
        root = etree.fromstring(f"<root>{xml_string}</root>")
        return len(root.findall(".//value"))
    except:
        return None

# fact_match
print("Transforming fact_match...")
fact_match = df_match[[
    "match_api_id", "country_id", "league_id", "season",
    "stage", "date", "home_team_api_id", "away_team_api_id",
    "home_team_goal", "away_team_goal", "shoton", "shotoff",
    "foulcommit", "corner", "possession"
]].copy()

# Pase XML columns into counts
print("   Parsing XML columns...")
fact_match["shoton"]    = fact_match["shoton"].apply(lambda x: parse_xml_count(x, "shoton"))
fact_match["shotoff"]   = fact_match["shotoff"].apply(lambda x: parse_xml_count(x, "shotoff"))
fact_match["foulcommit"] = fact_match["foulcommit"].apply(lambda x: parse_xml_count(x, "foulcommit"))
fact_match["corner"] = fact_match["corner"].apply(lambda x: parse_xml_count(x, "corner"))
fact_match["possession"] = fact_match["possession"].apply(lambda x: parse_xml_count(x, "possession"))

fact_match["date_id"] = pd.to_datetime(fact_match["date"]).dt.strftime("%Y%m%d").astype(int)
fact_match = fact_match.drop(columns=["date"])
fact_match = fact_match.dropna(subset=["match_api_id", "home_team_goal", "away_team_goal"])

# Save to warehouse folder
os.makedirs("data/warehouse", exist_ok=True)

dim_country.to_csv("data/warehouse/dim_country.csv", index=False)
dim_league.to_csv("data/warehouse/dim_league.csv", index=False)
dim_team.to_csv("data/warehouse/dim_team.csv", index=False)
dim_player.to_csv("data/warehouse/dim_player.csv", index=False)
dim_date.to_csv("data/warehouse/dim_date.csv", index=False)
fact_match.to_csv("data/warehouse/fact_match.csv", index=False)

print("Transformation complete. Files saved to data/warehouse/")
print(f"    dim_country: {len(dim_country)} rows")
print(f"    dim_league: {len(dim_league)} rows")
print(f"    dim_team: {len(dim_team)} rows")
print(f"    dim_player: {len(dim_player)} rows")
print(f"    dim_date: {len(dim_date)} rows")
print(f"    fact_match: {len(fact_match)} rows")