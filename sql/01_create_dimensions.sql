-- Country --
CREATE TABLE dim_country (
    country_id      INTEGER PRIMARY KEY,
    country_name    VARCHAR(100) NOT NULL
);

-- League --
CREATE TABLE dim_league (
    league_id   INTEGER PRIMARY KEY,
    league_name VARCHAR(100) NOT NULL,
    country_id  INTEGER NOT NULL,
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id)
);

-- Team --
CREATE TABLE dim_team (
    team_api_id         INTEGER PRIMARY KEY,
    team_fifa_api_id    INTEGER, 
    team_long_name      VARCHAR(100) NOT NULL,
    team_short_name     VARCHAR(100) NOT NULL
);

-- Player --
CREATE TABLE dim_player (
    player_api_id       INTEGER PRIMARY KEY,
    player_name         VARCHAR(150) NOT NULL,
    player_fifa_api_id  INTEGER,
    birthday            DATE,
    height              DECIMAL(5,2),
    weight              DECIMAL(5,2)
);

-- Date --
CREATE TABLE dim_date (
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

-- Fact Match --
CREATE TABLE fact_match (
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



