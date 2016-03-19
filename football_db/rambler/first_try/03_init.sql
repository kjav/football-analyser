-- rambler up

CREATE TABLE PlayedIn (
    Id bigserial PRIMARY KEY,
    Player bigserial REFERENCES Player(Id) NOT NULL,
    Team bigserial REFERENCES Team(Id),
    Match bigserial REFERENCES Match(Id) NOT NULL,
    Events jsonb
);

-- rambler down

DROP TABLE PlayedIn;
