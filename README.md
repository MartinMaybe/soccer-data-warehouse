# ⚽ Soccer Data Warehouse

A end-to-end data warehouse project built on European soccer match data. Raw data from a Kaggle SQLite database is extracted, transformed, and loaded into a PostgreSQL star schema warehouse using Python, ready for analytics and reporting.

---

## Project Overview

This project simulates a real-world data engineering workflow. Starting from a raw, messy dataset, it builds a clean, structured warehouse using standard concepts including medallion architecture, star schema design, and ETL pipeline development.

**Data Source:** [European Soccer Database](https://www.kaggle.com/datasets/hugomathien/soccer) by Hugo Mathien (Kaggle)

---

## Architecture

```
Raw Kaggle SQLite

       │
       ▼
Bronze Layer     
- staging as CSVs
- 01_extract.py: Pulls raw tables into /data/

       │
       ▼
Silver Layer    
- builds star schema
- 02_transform.py → Cleans, reshapes, parses XML

       │
       ▼
Gold Layer      
- warehouse
- 03_load.py → Loads clean data into PostgreSQL 

       │
       ▼

PostgreSQL
soccer_dw
```

---

## Data Model (Star Schema)

```
                        ┌─────────────┐
                        │  dim_date   │
                        │─────────────│
                        │ date_id  PK │
                        │ match_date  │
                        │ year        │
                        │ month       │
                        │ quarter     │
                        │ season      │
                        └──────┬──────┘
                               │
┌─────────────┐         ┌──────▼──────┐         ┌─────────────┐
│  dim_team   │         │ fact_match  │         │ dim_league  │
│─────────────│         │─────────────│         │─────────────│
│team_api_id  │◄────────│home_team_fk │         │ league_id PK│
│team_long_   │         │away_team_fk │────────►│ league_name │
│  name       │◄────────│league_id_fk │         │ country_id  │
│team_short_  │         │country_id_fk│         └──────┬──────┘
│  name       │         │date_id_fk   │                │
└─────────────┘         │home_goal    │         ┌──────▼──────┐
                        │away_goal    │         │dim_country  │
                        │shoton       │         │─────────────│
                        │shotoff      │         │ country_id  │
                        │foulcommit   │         │ country_name│
                        │corner       │         └─────────────┘
                        │possession   │
                        └─────────────┘
```

### Tables

| Table | Rows | Description |
|---|---|---|
| `fact_match` | 25,979 | One row per match with goals, shots, fouls, and corners |
| `dim_team` | 299 | Team names and IDs |
| `dim_player` | 11,060 | Player names, DOB, height, weight |
| `dim_league` | 11 | League names linked to country |
| `dim_country` | 11 | Country reference |
| `dim_date` | 1,694 | Full date spine with year, month, quarter, day of week |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | ETL scripting |
| pandas | Data manipulation and transformation |
| SQLite | Raw data source |
| PostgreSQL 18 | Data warehouse |
| SQLAlchemy | Python to PostgreSQL connection |
| psycopg2 | PostgreSQL database driver |
| lxml | XML parsing for match event data |
| pgAdmin 4 | Database UI and query tool |

---

## How to Run

### Prerequisites
- Python 3.x
- PostgreSQL 18
- pip packages: `pip3 install pandas sqlalchemy psycopg2-binary lxml`

### Setup

1. Clone the repo
```bash
git clone https://github.com/MartinMaybe/soccer-data-warehouse.git
cd soccer-data-warehouse
```

2. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/hugomathien/soccer) and place `database.sqlite` in `data/raw/`

3. Create the PostgreSQL database
```bash
psql postgres
CREATE DATABASE soccer_dw;
\q
```

4. Run the DDL to create tables (in pgAdmin or psql)
```sql
-- Run in order
\i sql/01_create_dimensions.sql
\i sql/02_create_facts.sql
```

5. Run the ETL pipeline
```bash
python3 etl/01_extract.py
python3 etl/02_transform.py
python3 etl/03_load.py
```

---

## Sample Queries

```sql
-- Top 10 highest scoring teams (home goals)
SELECT 
    t.team_long_name,
    SUM(f.home_team_goal) as total_home_goals
FROM fact_match f
JOIN dim_team t ON f.home_team_api_id = t.team_api_id
GROUP BY t.team_long_name
ORDER BY total_home_goals DESC
LIMIT 10;

-- Average goals per match by league
SELECT
    l.league_name,
    ROUND(AVG(f.home_team_goal + f.away_team_goal), 2) as avg_goals_per_match
FROM fact_match f
JOIN dim_league l ON f.league_id = l.league_id
GROUP BY l.league_name
ORDER BY avg_goals_per_match DESC;

-- Match results by season
SELECT
    season,
    COUNT(*) as total_matches,
    SUM(home_team_goal) as total_goals
FROM fact_match
GROUP BY season
ORDER BY season;
```

---

## Author

Martin — built as a portfolio project to demonstrate data engineering skills including ETL pipeline development, dimensional modeling, and data warehouse design.