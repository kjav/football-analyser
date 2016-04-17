from selenium import webdriver

everton_match_url = "http://www.whoscored.com/Matches/614052/Live"
python_url = "http://www.python.org"

driver = webdriver.Firefox()
driver.get(everton_match_url)
html_source = driver.page_source
print html_source.encode("utf-8")
driver.close()
