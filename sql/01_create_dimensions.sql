/*
01_create_dimensions.sql - Dimension Table DDL
===============================================
Creates all dimension tables for the soccer_dw star schema.

Must be run BEFORE 02_create_facts.sql since fact_match contains
foreign key references to these dimension tables.

Tables Created:
    - dim_country   Country reference data
    - dim_league    League names linked to country
    - dim_team      Team names and API identifiers
    - dim_player    Player profiles including DOB, height, weight
    - dim_date      Date spine with year, month, quarter, day of week

All CREATE TABLE statements use IF NOT EXISTS so this script
can be re-run safely without errors.

Run Order:
    1. sql/01_create_dimensions.sql
    2. sql/02_create_facts.sql
*/

-- Country --
CREATE TABLE IF NOT EXISTS dim_country (
    country_id      INTEGER PRIMARY KEY,
    country_name    VARCHAR(100) NOT NULL
);

-- League --
CREATE TABLE IF NOT EXISTS dim_league (
    league_id   INTEGER PRIMARY KEY,
    league_name VARCHAR(100) NOT NULL,
    country_id  INTEGER NOT NULL,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id)
);

-- Team --
CREATE TABLE IF NOT EXISTS dim_team (
    team_api_id         INTEGER PRIMARY KEY,
    team_fifa_api_id    INTEGER, 
    team_long_name      VARCHAR(100) NOT NULL,
    team_short_name     VARCHAR(100) NOT NULL
);

-- Player --
CREATE TABLE IF NOT EXISTS dim_player (
    player_api_id       INTEGER PRIMARY KEY,
    player_name         VARCHAR(150) NOT NULL,
    player_fifa_api_id  INTEGER,
    birthday            DATE,
    height              DECIMAL(5,2),
    weight              DECIMAL(5,2)
);

-- Date --
CREATE TABLE IF NOT EXISTS dim_date (
    date_id     INTEGER PRIMARY KEY,
    match_date  DATE NOT NULL,
    year        INTEGER NOT NULL,
    month       INTEGER NOT NULL, 
    month_name  VARCHAR(20) NOT NULL, 
    quarter     INTEGER NOT NULL,
    day         INTEGER NOT NULL, 
    day_of_week VARCHAR(20) NOT NULL,
    season      VARCHAR(20) NOT NULL
);