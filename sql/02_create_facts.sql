/*
02_create_facts.sql - Fact Table DDL
======================================
Creates the fact table for the soccer_dw star schema.

Must be run after 01_create_dimensions.sql since fact_match
contains foreign key references to all dimension tables.

Tables Created:
    - fact_match    One row per match containing goals, shots,
                    fouls, corners, and foreign keys to all
                    dimension tables.

Foreign Keys:
    - date_id           dim_date(date_id)
    - country_id        dim_country(country_id)
    - league_id         dim_league(league_id)
    - home_team_api_id  dim_team(team_api_id)
    - away_team_api_id  dim_team(team_api_id)

*/

-- Fact Match --
CREATE TABLE IF NOT EXISTS fact_match (
    match_api_id        INTEGER PRIMARY KEY,
    date_id             INTEGER NOT NULL,
    country_id          INTEGER NOT NULL,
    league_id           INTEGER NOT NULL,
    season              VARCHAR(20) NOT NULL,
    stage               INTEGER NOT NULL,
    home_team_api_id    INTEGER NOT NULL,
    away_team_api_id    INTEGER NOT NULL,
    home_team_goal      INTEGER NOT NULL,
    away_team_goal      INTEGER NOT NULL,
    shoton              INTEGER,
    shotoff             INTEGER,
    foulcommit          INTEGER,
    corner              INTEGER,
    possession          DECIMAL(5,2),
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),
    FOREIGN KEY (league_id) REFERENCES dim_league(league_id),
    FOREIGN KEY (home_team_api_id) REFERENCES dim_team(team_api_id),
    FOREIGN KEY (away_team_api_id) REFERENCES dim_team(team_api_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);