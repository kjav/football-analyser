import re
import json
#from selenium import webdriver


# These are all the regex's to get the JSON from the page source
allRegionsReg = re.compile("var allRegions = (?P<data>\[.*?\]);", re.DOTALL)
matchCentreDataReg = re.compile("var matchCentreData = (?P<data>.*?);", re.DOTALL)
matchCentreEventTypeJsonReg = re.compile("var matchCentreEventTypeJson = (?P<data>.*?);", re.DOTALL)
matchIdReg = re.compile("var matchId = (?P<data>.*?);", re.DOTALL)
formationIdNameMappingsReg = re.compile("var formationIdNameMappings = (?P<data>.*?);", re.DOTALL)

def get_JSON(page_source):
    unprocessedregions = allRegionsReg.search(page_source)
    allRegions = unprocessedregions.group("data") if unprocessedregions else '{}'

    unprocessedMatchCentreData = matchCentreDataReg.search(page_source)
    MatchCentreData =  unprocessedMatchCentreData.group("data") if unprocessedMatchCentreData else '{}'

    unprocEventType = matchCentreEventTypeJsonReg.search(page_source)
    EventType  = unprocEventType.group("data") if unprocEventType else '{}'

    unprocid = matchIdReg.search(page_source, re.DOTALL)
    matchId = unprocid.group("data") if unprocid else '{}'

    unprocform = formationIdNameMappingsReg.search(page_source, re.DOTALL)
    formationIdMapping = unprocform.group("data") if unprocform else '{}'

    unpretty = '{"matchId":' + matchId + ',"allRegions":' + '"'+ "" + '"' + ',"matchCentreData":' + MatchCentreData + ',"matchCentreEventTypeJson":' + EventType + ',"formationIdNameMappings":' + formationIdMapping + '}'
    decoded = json.loads(unpretty)
    pretty = json.dumps(decoded, indent=4, sort_keys=True)
    return pretty

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
"""

test = open("everton_source.html")
html_source = test.read()
test.close()
print get_JSON(html_source)

