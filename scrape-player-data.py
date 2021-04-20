import sqlite3 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from config import DRIVER_PATH, LEAGUE_ID

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

url = "https://fantasy.nfl.com/league/" + LEAGUE_ID + "/players"
driver.get(url)

# A custom expected condition class that evaluates whether
# an element's attribute equals a given value. 
class wait_for_attribute_value(object):
    def __init__(self, locator, attribute, value):
        self.locator = locator
        self.attribute = attribute
        self.value = value

    def __call__(self, driver):
        try:
            element_attribute = EC._find_element(driver, self.locator).get_attribute(self.attribute)
            return element_attribute == self.value
        except StaleElementReferenceException:
            return False

# A custom expected condition class that evaluates whether
# an element has a given attribute. 
class wait_for_attribute(object):
    def __init__(self, locator, attribute):
        self.locator = locator
        self.attribute = attribute

    def __call__(self, driver):
        try:
            element_attribute = EC._find_element(driver, self.locator).get_attribute(self.attribute)
            return element_attribute != None
        except StaleElementReferenceException:
            return False

# Click to load data for all players, not just available players. 
driver.find_element_by_xpath("//select[@id='playerStatus']/option[text()='All Players']").click()
WebDriverWait(driver, 5, ignored_exceptions=(StaleElementReferenceException)).until(wait_for_attribute((By.XPATH, "//select[@id='playerStatus']/option[text()='All Players']"), "selected"))

# Click to load only receiver data. 
driver.find_element_by_id("pos3").click()
WebDriverWait(driver, 5, ignored_exceptions=(StaleElementReferenceException)).until(wait_for_attribute_value((By.XPATH, "//li[@id='pos3']"), "class", "selected"))

# Extract data from the table of players. 
html = BeautifulSoup(driver.page_source, 'html.parser')
receiversHtml = html.find_all('a', { 'class': 'playerCard' })

# Parses text into a numeric value, returning 
# 0 for missing data. 
def parseFloat(string):
    try:
        return float(string)
    except ValueError:
        return 0

db = sqlite3.connect('webapp/data.db')
cursor = db.cursor()

# Create database table to store player data. 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Player (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(255),
        passYards FLOAT,
        passTouchdowns FLOAT,
        interceptions FLOAT,
        rushYards FLOAT,
        rushTouchdowns FLOAT,
        receptions FLOAT,
        receivingYards FLOAT,
        receivingTouchdowns FLOAT,
        points FLOAT
    )
""")

# Add receiver stats to a list. 
receivers = []
for receiverNameElement in receiversHtml:
    row = receiverNameElement.parent.parent.parent
    stats = { 'name': receiverNameElement.text }

    passingStats = {}
    passingStats['yards'] = parseFloat(row.find('td', { 'class': 'stat_5' }).text)
    passingStats['touchdowns'] = parseFloat(row.find('td', { 'class': 'stat_6' }).text)
    passingStats['interceptions'] = parseFloat(row.find('td', { 'class': 'stat_7' }).text)
    stats['passing'] = passingStats

    rushingStats = {}
    rushingStats['yards'] = parseFloat(row.find('td', { 'class': 'stat_14' }).text)
    rushingStats['touchdowns'] = parseFloat(row.find('td', { 'class': 'stat_15' }).text)
    stats['rushing'] = rushingStats

    receivingStats = {}
    receivingStats['receptions'] = parseFloat(row.find('td', { 'class': 'stat_20' }).text)
    receivingStats['yards'] = parseFloat(row.find('td', { 'class': 'stat_21' }).text)
    receivingStats['touchdowns'] = parseFloat(row.find('td', { 'class': 'stat_22' }).text)
    stats['receiving'] = receivingStats
    
    stats['points'] = parseFloat(row.find('td', { 'class': 'statTotal' }).text)

    cursor.execute("""
        INSERT INTO Player (name, passYards, passTouchdowns, interceptions, rushYards, rushTouchdowns, receptions, receivingYards, receivingTouchdowns, points) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (stats['name'], stats['passing']['yards'], stats['passing']['touchdowns'], stats['passing']['interceptions'], stats['rushing']['yards'], stats['rushing']['touchdowns'], stats['receiving']['receptions'], stats['receiving']['yards'], stats['receiving']['touchdowns'], stats['points']))
    db.commit() 

    receivers.append(stats)

db.close()

driver.quit()