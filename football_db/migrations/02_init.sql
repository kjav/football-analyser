-- rambler up

CREATE TABLE match (
    id bigserial PRIMARY KEY,
    stage bigserial REFERENCES stage(id) NOT NULL,
    home_team bigserial REFERENCES team(id) NOT NULL,
    away_team bigserial REFERENCES team(id) NOT NULL,
    result bigserial REFERENCES result(id),
    the_date date NOT NULL
);

CREATE TABLE probableLineUp (
    id bigserial PRIMARY KEY,
    matchid bigserial REFERENCES match(id) NOT NULL,
    teamid bigserial REFERENCES team(id) NOT NULL,
    player1id REFERENCES player(id) NOT NULL,
    player2id REFERENCES player(id) NOT NULL,
    player3id REFERENCES player(id) NOT NULL,
    player4id REFERENCES player(id) NOT NULL,
    player5id REFERENCES player(id) NOT NULL,
    player6id REFERENCES player(id) NOT NULL,
    player7id REFERENCES player(id) NOT NULL,
    player8id REFERENCES player(id) NOT NULL,
    player9id REFERENCES player(id) NOT NULL,
    player10id REFERENCES player(id) NOT NULL,
    player11id REFERENCES player(id) NOT NULL
);

-- rambler down

DROP TABLE match;
DROP TABLE probableLineUp;
