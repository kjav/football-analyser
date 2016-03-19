-- rambler up

CREATE TABLE Season (
    Id bigserial PRIMARY KEY,
    Country text,
    League text,
    StartDate date,
    EndDate date
);

CREATE TABLE Match (
    Id bigserial PRIMARY KEY,
    HomeTeam bigserial REFERENCES Team(Id) NOT NULL,
    AwayTeam bigserial REFERENCES Team(Id) NOT NULL,
    DateAndTime timestamp,
    Season bigserial REFERENCES Season(Id) NOT NULL,
    League bigserial REFERENCES League(Id) NOT NULL,
    Result integer
);

-- rambler down

DROP TABLE Match;
DROP TABLE Season;
