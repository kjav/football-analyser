import json
import psycopg2
import re
import pprint
from datetime import datetime

# dd/mm/yyyy to mm/dd/yyyy
def conv_date(date) :
    return datetime.strptime(date, "%d/%m/%Y %H:%M:%S")

# get the matchids which haven't been processed yet
# assume matches in the match table have already got
# TeamMatches and PlayerMatches linked up
# This may be a dubious assumption
def get_match_ids(curs):
    curs.execute("CREATE TABLE IF NOT EXISTS processed_json_match (matchid bigserial REFERENCES match(id));")
    curs.execute("CREATE TABLE IF NOT EXISTS event (id bigserial PRIMARY KEY, data jsonb, matchid bigint REFERENCES match(id));")
    curs.execute("CREATE TABLE IF NOT EXISTS event_type (typeid bigserial PRIMARY KEY, name text);")
    curs.execute("CREATE TABLE IF NOT EXISTS event_type_satisfied (eventId bigint REFERENCES event(id), typeid bigint REFERENCES event_type(typeid));")

    curs.execute("SELECT matchid FROM processed_json_match;")
    rows = curs.fetchall()
    processed = map(lambda x: x[0], rows)

    curs.execute("SELECT match_id FROM match_json;")
    rows = curs.fetchall()
    crawled_ids = map(lambda x: x[0], rows)
    matches = set(crawled_ids) - set(processed)
    print "processing matches: ", matches
    return matches

# given an id, get the raw json corresponding
# to that match
def get_match_json(id, curs):
    curs.execute("SELECT data FROM match_json WHERE match_id = %s;", (id, ))
    rows = curs.fetchall()
    if rows == [] :
        return None
    else :
        return json.loads(rows[0][0])

def sumdict(dic, s) :
    return sum(dic[s].values())

def createteammatch(data, team, goals):
    stats = data['matchCentreData'][team]['stats']
    result = {
        'tm_id' : None,
        'Rating' : stats['ratings'][max(stats['ratings'].iterkeys())],
        'Goals' : goals,
        'ThroughBall' : None,
        'OwnGoals' : None,
        'TotalTackle' : sum(stats['tacklesTotal'].values())
    }

    result['teamId'] = data['matchCentreData'][team]['teamId']
    result['matchId'] = data['matchId']
    result['TotalScoringAttempts'] = sum(stats['shotsTotal'].values())
    if 'shotsOnTarget' in stats :
        result['ShotsOnTarget'] = sum(stats['shotsOnTarget'].values())
    else:
        result['ShotsOnTarget'] = None
    result['KeyPass'] = sum(stats['passesKey'].values())
    result['TotalPass'] = sum(stats['passesTotal'].values())
    result['AccuratePass'] = sum(stats['passesAccurate'].values())
    result['TotalClearance'] = sum(stats['clearances'].values())
    result['Interceptions'] = sum(stats['interceptions'].values())
    result['AerialWon'] = sum(stats['aerialsWon'].values())
    print "teammatch: "
    pprint.pprint(result)
    return result

def createplayermatches(data, team, cur):
    players = data['matchCentreData'][team]['players']
    result = []
    for player in players :
        stats = player['stats']
        try:
            player_goals = 0
            cur.execute("SELECT event.data FROM event, event_type, event_type_satisfied WHERE event_type_satisfied.eventid = event.id AND event_type.typeid = event_type_satisfied.typeid AND event_type.name = 'goalNormal';")
            for e in cur.fetchall() :
                e = json.loads(e[0])
                if player['playerId'] == e['playerId']:
                    player_goals += 1
            a = set()
            for stat in stats.itervalues() :
                a | set(stat.iterkeys())
            minsplayed = len(a)
            b = {
                'Position' : player['position'],
                'tm_id' : None,
                'pm_id' : None,
                'Goals' : player_goals,
                'Rating': stats['ratings'][max(stats['ratings'].iterkeys())],
                'MinutesPlayed' : minsplayed,
                'ThroughBalls' : None,
                'playerId' : player['playerId'],
                'TotalScoringAttempts' : sumdict(stats, 'shotsTotal') if 'shotsTotal' in stats else 0,
                'ShotsOnTarget' :  sumdict(stats, 'shotsOnTarget') if 'shotsOnTarget' in stats else 0,
                'KeyPass' :  sumdict(stats, 'passesKey') if 'passesKey' in stats else 0,
                'TotalPass' :  sumdict(stats, 'passesTotal') if 'passesTotal' in stats else 0,
                'AccuratePass' :  sumdict(stats, 'passesAccurate') if 'passesAccurate' in stats else 0,
                'TotalTackle' :  sumdict(stats, 'tacklesTotal') if 'tacklesTotal' in stats else 0,
                'TotalClearance' :  sumdict(stats, 'clearances') if 'clearances' in stats else 0,
                'Interceptions' :  sumdict(stats, 'interceptions') if 'interceptions' in stats else 0,
                'AerialWon' :  sumdict(stats, 'aerialsWon') if 'aerialsWon' in stats else 0
            }
            result.append(b)
        except KeyError:
            print "key error with this player:"
            pprint.pprint(player)
    print "players: "
    pprint.pprint(result)
    return result

def deal_with_events(data, cur):
    events = data['matchCentreData']['events']
    matchid = data['matchId']
    print "inserting events....."
    for e in events :
        eventid = int(e['id'])
        cur.execute("SELECT * FROM event WHERE id = %s;", (eventid,))
        a = cur.fetchall()
        if a == [] :
            cur.execute("INSERT INTO event(id, data, matchid) VALUES(%s, %s, %s);", (eventid, json.dumps(e), matchid))
            for i in e['satisfiedEventsTypes']:
                cur.execute("INSERT INTO event_type_satisfied(typeid, eventid) VALUES(%s, %s);", (i, eventid))

def add_teammatch_to_db(data, cur):
    matchId = data['matchId']
    teamId = data['teamId']
    SQL = "INSERT INTO team_match VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cur.execute("SELECT id FROM team_match WHERE team = %s AND match = %s", (teamId, matchId))
    if cur.fetchall() == []:
        cur.execute(SQL, (teamId, matchId, data['Rating'], data['Goals'], data['TotalScoringAttempts'], data['ShotsOnTarget'], data['ThroughBall'], data['KeyPass'], data['TotalPass'], data['AccuratePass'], data['TotalTackle'], data['TotalClearance'], data['Interceptions'], data['AerialWon'], data['OwnGoals']))
    cur.execute("SELECT id FROM team_match WHERE team=%s AND match = %s;",(teamId, matchId))
    return cur.fetchall()[0][0]

def add_playermatch_to_db(data, cur, tm_id):
    for player in data :
        cur.execute("SELECT * FROM player_match WHERE playerid = %s AND teammatchid = %s;", (player['playerId'], tm_id))
        if cur.fetchall() == [] :
            cur.execute("INSERT INTO player_match VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",
                        (player['playerId'], tm_id, player['Rating'], player['Position'], player['Goals'], player['TotalScoringAttempts'], player['ShotsOnTarget'], player['ThroughBalls'], player['KeyPass'], player['TotalPass'], player['AccuratePass'], player['TotalTackle'], player['TotalClearance'], player['Interceptions'], player['AerialWon'], player['MinutesPlayed']))

def process_match_json(data, cur):
    # add eventTypeIds
    eventType = data['matchCentreEventTypeJson']
    for typename, typeid in eventType.items():
        cur.execute("SELECT * FROM event_type WHERE typeid = %s;", (typeid,))
        a = cur.fetchall()
        if a == [] :
            print "inserting event type:", typename, " ", typeid
            cur.execute("INSERT INTO event_type(typeid, name) VALUES(%s, %s);", (typeid, typename))

    centre = data['matchCentreData']
    # first make sure we have the players and team in the db,
    # inserting where necessary
    homeid = centre['home']['teamId']
    homename = centre['home']['name']
    awayid = centre['away']['teamId']
    awayname = centre['away']['name']

    # insert home and away teams if they don't exist
    SQL1 = "SELECT * FROM team WHERE id = %s;"
    SQL2 = "INSERT INTO team VALUES (%s, %s);"
    cur.execute(SQL1, (homeid,)) # is the homeid in the db?
    if cur.fetchall() == [] :
        cur.execute(SQL2,(homeid, homename)) #insert home team
        print "Inserted team: %s, %d into db" % (homename, homeid)
    cur.execute(SQL1, (awayid,))
    if cur.fetchall() == [] :
        cur.execute(SQL2, (awayid, awayname))
        print "Inserted team: %s, %d into db" % (awayname, awayid)
    # insert players if they don't exist
    players = centre['home']['players'] + centre['away']['players']
    for player in players :
        cur.execute("SELECT * FROM player WHERE ID = %s;", (player['playerId'],))
        if cur.fetchall() == [] :
            print "inserting player ", player['name'], "into db with id: ", player['name']
            cur.execute("INSERT INTO player(id, name, height, age, position) VALUES(%s, %s, %s, %s, %s);",(player['playerId'], player['name'],player['height'], player['age'], player['position']))

    # create result for match
    score = re.match("(?P<home>[0-9]*) : (?P<away>[0-9]*)", centre['score'])
    date = centre['timeStamp']

    # insert match id if it doesn't exist
    cur.execute("SELECT * FROM match WHERE id = %s;", (data['matchId'],))
    if cur.fetchall() == []:
        cur.execute("INSERT INTO result(id, home_goals, away_goals) VALUES(DEFAULT, %s, %s) RETURNING id;",
                    (score.group("home"), score.group("away"),))
        resultId = cur.fetchone()[0]
        print "result id: %d" % resultId
        cur.execute("SELECT * FROM team WHERE id = %s OR id = %s;", (homeid, awayid))
        print cur.fetchall()
        cur.execute("SELECT * FROM result where id = %s;", (resultId,))
        print cur.fetchall()
        cur.execute("INSERT INTO match(id, stage, home_team, away_team, result, the_date) Values(%s, %s, %s, %s, %s, %s);",
                    (data['matchId'], 1, homeid, awayid, resultId, date))

    deal_with_events(data, cur)

    print "creating dictionaries...."
    away_teammatch = createteammatch(data, "away", score.group("away"))
    home_teammatch = createteammatch(data, "home", score.group("home"))

    away_players = createplayermatches(data, "away", cur)
    home_players = createplayermatches(data, "home", cur)

    print "adding dictionaries to database...."
    away_tm_id = add_teammatch_to_db(away_teammatch, cur)
    home_tm_id = add_teammatch_to_db(home_teammatch, cur)

    add_playermatch_to_db(home_players, cur, home_tm_id)
    add_playermatch_to_db(away_players, cur, away_tm_id)

def main():
    server_details = "dbname=test user=coxswain password=Torpids2016 host=football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com port=5432"
    print "Connecting to database\n	->%s" % (server_details)
    conn = psycopg2.connect(server_details)
    cur = conn.cursor()

    try:
        match_ids = get_match_ids(cur)
    except Exception as e:
        cur.close()
        conn.close()
        raise e

    print "match_ids being processed: %s" % (match_ids)
    conn.commit()
    for i in match_ids :
        print "Processing match %d" % i
        try:
            data = get_match_json(i, cur)
            process_match_json(data, cur)
        except:
            cur.close()
            conn.close()
            raise
        else:
            print "processed"
            cur.execute("INSERT INTO processed_json_match VALUES(%s);", (data['matchId'],))
            conn.commit()

    cur.close()
    conn.close()

if __name__ == "__main__" :
    main()
