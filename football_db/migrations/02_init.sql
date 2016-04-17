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
    teamid bigserial REFERENCES team(id) NOT NULL,
    player1id bigserial REFERENCES player(id),
    player2id bigserial REFERENCES player(id),
    player3id bigserial REFERENCES player(id),
    player4id bigserial REFERENCES player(id),
    player5id bigserial REFERENCES player(id),
    player6id bigserial REFERENCES player(id),
    player7id bigserial REFERENCES player(id),
    player8id bigserial REFERENCES player(id),
    player9id bigserial REFERENCES player(id),
    player10id bigserial REFERENCES player(id),
    player11id bigserial REFERENCES player(id)
);

-- rambler down

DROP TABLE match;
DROP TABLE probableLineUp;
