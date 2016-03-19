-- rambler up

CREATE TABLE Team (
    Id bigserial PRIMARY KEY,
    Name text UNIQUE NOT NULL
);


CREATE TABLE Player (
    Id bigserial PRIMARY KEY,
    Name text NOT NULL
);

CREATE TABLE League (
    Id bigserial PRIMARY KEY,
    Name text UNIQUE NOT NULL
);

-- rambler down

DROP TABLE Team;
DROP TABLE Player;
DROP TABLE League;
