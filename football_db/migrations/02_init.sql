-- rambler up

CREATE TABLE match (
    id bigserial PRIMARY KEY,
    stage bigserial REFERENCES stage(id) NOT NULL,
    home_team bigserial REFERENCES team(id) NOT NULL,
    away_team bigserial REFERENCES team(id) NOT NULL,
    result bigserial REFERENCES result(id),
    the_date date NOT NULL
);

-- rambler down

DROP TABLE match;
