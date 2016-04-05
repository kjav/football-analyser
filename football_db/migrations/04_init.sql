-- rambler up

CREATE TABLE player_match (
    id bigserial PRIMARY KEY,
    playerid bigserial REFERENCES player(id) NOT NULL,
    teammatchid bigserial REFERENCES match(id) NOT NULL,
    rating NUMERIC(6,3),
    Position VARCHAR(40),
    Goals SMALLINT,
    TotalScoringAttempts SMALLINT,
    ShotsOnTarget SMALLINT,
    ThroughBalls SMALLINT,
    KeyPass SMALLINT,
    TotalPass SMALLINT,
    AccuratePass SMALLINT,
    TotalTackle SMALLINT,
    TotalClearance SMALLINT,
    Interception SMALLINT,
    AerialWon SMALLINT);

-- rambler down

DROP TABLE player_match;
