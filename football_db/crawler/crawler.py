import re
import json
import binascii
from selenium import webdriver
import psycopg2
import pprint

# These are all the regex's to get the JSON from the page source
allRegionsReg = re.compile("var allRegions = (?P<data>\[.*?\]);", re.DOTALL)
matchCentreDataReg = re.compile("var matchCentreData = (?P<data>.*?);", re.DOTALL)
matchCentreEventTypeJsonReg = re.compile("var matchCentreEventTypeJson = (?P<data>.*?);", re.DOTALL)
matchIdReg = re.compile("var matchId = (?P<data>.*?);", re.DOTALL)
formationIdNameMappingsReg = re.compile("var formationIdNameMappings = (?P<data>.*?);", re.DOTALL)

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

    if (allRegions == '{}' || MatchCentreData == '{}' || EventType = '{}' || matchId == '{}' || formationIdMapping == '{}'):
        return None
    else:
        unpretty = '{"matchId":' + matchId + ',"allRegions":' + '"'+ allRegions + '"' + ',"matchCentreData":' + MatchCentreData + ',"matchCentreEventTypeJson":' + EventType + ',"formationIdNameMappings":' + formationIdMapping + '}'
        decoded = json.loads(unpretty)
        pretty = json.dumps(decoded, indent=4, sort_keys=True)
        return pretty

def get_raw_match(id, driver):
    url = "http://www.whoscored.com/Matches/{0}/Live".format(id)
    driver.get(url)
    return driver.page_source.encode("utf=8")

def put_in_db(data, id, cur):
    cur.execute("INSERT INTO match_json VALUES (%s, %s);", (id, data))

start = 0
end = 10
everton = 614052

everton_match_url = "http://www.whoscored.com/Matches/614052/Live"
python_url = "http://www.python.org"

"""
driver = webdriver.Firefox()
driver.get(everton_match_url)
html_source = driver.page_source
print get_JSON(html_source.encode("utf-8"))
driver.close()

test = open("everton_source.html")
html_source = test.read()
test.close()
print get_JSON(html_source)
"""

server_details = "dbname=test user=coxswain password=Torpids2016 host=football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com port=5432"

conn = psycopg2.connect(server_details)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS match_json (match_id bigserial PRIMARY KEY, data jsonb);")
conn.commit()
driver = webdriver.Firefox()

for num in range(everton,everton+2):
    a = get_raw_match(num, driver)
    b = get_JSON(a)
    if b:
        put_in_db(b, num, cur)
        conn.commit()

cur.close()
conn.close()
driver.close()
