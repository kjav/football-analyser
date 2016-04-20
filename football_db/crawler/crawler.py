import re
import json
import binascii
from selenium import webdriver
import selenium
import psycopg2

# These are all the regex's to get the JSON from the page source
allRegionsReg = re.compile("var allRegions = (?P<data>\[.*?\]);", re.DOTALL)
matchCentreDataReg = re.compile("var matchCentreData = (?P<data>.*?);", re.DOTALL)
matchCentreEventTypeJsonReg = re.compile("var matchCentreEventTypeJson = (?P<data>.*?);", re.DOTALL)
matchIdReg = re.compile("var matchId = (?P<data>.*?);", re.DOTALL)
formationIdNameMappingsReg = re.compile("var formationIdNameMappings = (?P<data>.*?);", re.DOTALL)

# given the html file for the match, return a json string with the information
def get_JSON(page_source):
    unprocessedregions = allRegionsReg.search(page_source)
    allRegions = unprocessedregions.group("data") if unprocessedregions else '{}'
    allRegions = binascii.hexlify(allRegions)

    unprocessedMatchCentreData = matchCentreDataReg.search(page_source)
    MatchCentreData =  unprocessedMatchCentreData.group("data") if unprocessedMatchCentreData else '{}'

    unprocEventType = matchCentreEventTypeJsonReg.search(page_source)
    EventType  = unprocEventType.group("data") if unprocEventType else '{}'

    unprocid = matchIdReg.search(page_source, re.DOTALL)
    matchId = unprocid.group("data") if unprocid else '{}'

    unprocform = formationIdNameMappingsReg.search(page_source, re.DOTALL)
    formationIdMapping = unprocform.group("data") if unprocform else '{}'

    if (allRegions == '{}' or MatchCentreData == '{}' or EventType == '{}' or matchId == '{}' or formationIdMapping == '{}'):
        return None
    else:
        unpretty = '{"matchId":' + matchId + ',"allRegions":' + '"'+ allRegions + '"' + ',"matchCentreData":' + MatchCentreData + ',"matchCentreEventTypeJson":' + EventType + ',"formationIdNameMappings":' + formationIdMapping + '}'
        decoded = json.loads(unpretty)
        pretty = json.dumps(decoded, indent=4, sort_keys=True)
        return pretty

# given a match id, get the html file for it
def get_raw_match(id, driver):
    url = "http://www.whoscored.com/Matches/{0}/Live".format(id)
    driver.get(url)
    return driver.page_source.encode("utf=8")

# given a json file, put in in the database
def put_in_db(data, id, cur):
	cur.execute("DELETE FROM match_json WHERE match_id = %s;", (id,))
	cur.execute("INSERT INTO match_json VALUES (%s, %s);", (id, data))

#get the match ids that haven't been crawled.
def get_match_ids(curs):
    idsfile = open("ids.json", "r")
    ids = json.load(idsfile)
    idsfile.close()

    curs.execute("SELECT match_id FROM match_json;")
    rows = curs.fetchall()
    crawled_ids = map(lambda x: x[0], rows)
    return set(ids) - set(crawled_ids)

"""
crawled_ids = []
def register_crawl(matchid):
    print ""
"""

server_details = "dbname=test user=coxswain password=Torpids2016 host=football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com port=5432"
print "Connecting to database\n	->%s" % (server_details)
conn = psycopg2.connect(server_details)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS match_json (match_id bigserial PRIMARY KEY, data jsonb);")
conn.commit()
driver = webdriver.Firefox()
match_ids = get_match_ids(cur)
print "Crawling matches with these ids:\n"
print match_ids

for num in match_ids:
    print "attempting to get match: %d" % num
    try:
        a = get_raw_match(num, driver)
        b = get_JSON(a)
    except selenium.common.exceptions.TimeoutException:
        b = None
    if b:
        put_in_db(b, num, cur)
        conn.commit()
        print "successfully got data for match: %d" % num
    else:
        print "error in match %d"

cur.close()
conn.close()
driver.close()


