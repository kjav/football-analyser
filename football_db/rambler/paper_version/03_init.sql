-- rambler up

CREATE TABLE team_match (
    id bigserial PRIMARY KEY,
    team bigserial REFERENCES team(id) NOT NULL,
    match bigserial REFERENCES match(id) NOT NULL,
    rating integer,
    goals integer NOT NULL,
    total_passes integer,
    aerials_won integer,
    shots_on_goal integer,
    Fouls integer,
    yellow_cards integer,
    red_cards integer
);

-- rambler down

DROP TABLE team_match;
