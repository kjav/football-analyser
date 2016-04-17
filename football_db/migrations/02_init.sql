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
    player1id bigserial REFERENCES player(id) NOT NULL,
    player2id bigserial REFERENCES player(id) NOT NULL,
    player3id bigserial REFERENCES player(id) NOT NULL,
    player4id bigserial REFERENCES player(id) NOT NULL,
    player5id bigserial REFERENCES player(id) NOT NULL,
    player6id bigserial REFERENCES player(id) NOT NULL,
    player7id bigserial REFERENCES player(id) NOT NULL,
    player8id bigserial REFERENCES player(id) NOT NULL,
    player9id bigserial REFERENCES player(id) NOT NULL,
    player10id bigserial REFERENCES player(id) NOT NULL,
    player11id bigserial REFERENCES player(id) NOT NULL
);

-- rambler down

DROP TABLE match;
DROP TABLE probableLineUp;
