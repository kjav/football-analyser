-- rambler up

CREATE TABLE player_match (
    id bigserial PRIMARY KEY,
    player bigserial REFERENCES player(id) NOT NULL,
    rating integer,
    position text,
    goal integer,
    accurate_pass integer,
    aerials_won integer,
    shots_on_goal integer,
    fouls integer,
    yellow_cards integer,
    red_cards integer
);

-- rambler down

DROP TABLE player_match;
