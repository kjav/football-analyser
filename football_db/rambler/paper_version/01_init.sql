-- rambler up

CREATE TABLE team (
    id bigserial PRIMARY KEY,
    name text UNIQUE NOT NULL
);

CREATE TABLE player (
    id bigserial PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE stage (
    id bigserial PRIMARY KEY,
    country text NOT NULL,
    league text NOT NULL,
    year date NOT NULL
);

CREATE TABLE result (
    id bigserial PRIMARY KEY,
    home_goals integer NOT NULL,
    away_goals integer NOT NULL
);

-- rambler down

DROP TABLE team;
DROP TABLE player;
DROP TABLE stage;
DROP TABLE result;
