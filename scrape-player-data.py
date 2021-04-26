import psycopg2 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import DRIVER_PATH, LEAGUE_ID, DB, USER, PASSWORD

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

page = 1
playerOffset = 1 + 25 * (page - 1)
url = 'https://fantasy.nfl.com/league/' + LEAGUE_ID + '/players?offset=' + str(page) + '&playerStatus=all&position=3&sort=pts&sortOrder=desc&statCategory=stats&statSeason=2020&statType=seasonStats'
driver.get(url)

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

db = psycopg2.connect(dbname=DB, user=USER, password=PASSWORD)
cursor = db.cursor()

# Create database table to store player data. 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Player (
        id SERIAL PRIMARY KEY,
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
        INSERT INTO Player (name, passYards, passTouchdowns, interceptions, rushYards, rushTouchdowns, receptions, receivingYards, receivingTouchdowns, points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (stats['name'], stats['passing']['yards'], stats['passing']['touchdowns'], stats['passing']['interceptions'], stats['rushing']['yards'], stats['rushing']['touchdowns'], stats['receiving']['receptions'], stats['receiving']['yards'], stats['receiving']['touchdowns'], stats['points']))
    db.commit() 

    receivers.append(stats)

db.close()
driver.quit()