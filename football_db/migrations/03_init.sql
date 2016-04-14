-- rambler up

CREATE TABLE team_match (
    id bigserial PRIMARY KEY,
    team bigserial REFERENCES team(id) NOT NULL,
    match bigserial REFERENCES match(id) NOT NULL,
    rating NUMERIC(6,3),
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
    AerialWon SMALLINT,
    OwnGoals SMALLINT);

-- rambler down

DROP TABLE team_match;
