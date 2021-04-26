import math
import psycopg2 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from helpers import parseFloat
from config import DRIVER_PATH, LEAGUE_ID, DB, USER, PASSWORD

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

db = psycopg2.connect(dbname=DB, user=USER, password=PASSWORD)
cursor = db.cursor()

# Create database table to store player data. 
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Player (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        position VARCHAR(255),
        season SMALLINT,
        passYards REAL,
        passTouchdowns REAL,
        interceptions REAL,
        rushYards REAL,
        rushTouchdowns REAL,
        receptions REAL,
        receivingYards REAL,
        receivingTouchdowns REAL,
        points REAL
    )
""")

# Note: This dataset may include records for players in years
# they did not play. While all associated stats are 0 in these
# rows, the data should be cleaned to only include entries for 
# a player in the years they did play. 

# Extract data for all seasons since 2009. 
firstSeasonToInclude = 2009
lastSeasonToInclude = 2020
for season in range(firstSeasonToInclude, lastSeasonToInclude + 1):

    # Iterate over QB, RB, WR, and TE data. Specify how many players 
    # to collect data for each season. 
    positionKeys = { 1: 'QB', 2: 'RB', 3: 'WR', 4: 'TE' }
    rowsPerPosition = { 1: 25, 2: 50, 3: 50, 4: 25 }
    for playerPosition in (*positionKeys,):

        # Each page has data for 25 players, and the url requires 
        # the index of the first player on the current page. 
        for page in range(math.ceil(rowsPerPosition[playerPosition] / 25)):
            playerOffset = 1 + 25 * page
            url = f'https://fantasy.nfl.com/league/{LEAGUE_ID}/players' \
                  f'?offset={playerOffset}&playerStatus=all&position={playerPosition}' \
                  f'&sort=pts&sortOrder=desc&statCategory=stats&statSeason={season}' \
                  f'&statType=seasonStats'
            driver.get(url)

            # Extract data from the table of players. 
            html = BeautifulSoup(driver.page_source, 'html.parser')
            receiversHtml = html.find_all('a', { 'class': 'playerCard' })

            # Insert player stats into the database. 
            for receiverNameElement in receiversHtml:
                row = receiverNameElement.parent.parent.parent
                stats = [receiverNameElement.text, positionKeys[playerPosition], season]

                # Extract passing stats.
                stats.append(parseFloat(row.find('td', { 'class': 'stat_5' }).text))
                stats.append(parseFloat(row.find('td', { 'class': 'stat_6' }).text))
                stats.append(parseFloat(row.find('td', { 'class': 'stat_7' }).text))

                # Extract rushing stats. 
                stats.append(parseFloat(row.find('td', { 'class': 'stat_14' }).text))
                stats.append(parseFloat(row.find('td', { 'class': 'stat_15' }).text))

                # Extract receiving stats. 
                stats.append(parseFloat(row.find('td', { 'class': 'stat_20' }).text))
                stats.append(parseFloat(row.find('td', { 'class': 'stat_21' }).text))
                stats.append(parseFloat(row.find('td', { 'class': 'stat_22' }).text))
                
                # Extract total points. 
                stats.append(parseFloat(row.find('td', { 'class': 'statTotal' }).text))

                cursor.execute("""
                    INSERT INTO Player 
                        (name, position, season, 
                         passYards, passTouchdowns, interceptions, 
                         rushYards, rushTouchdowns, receptions, 
                         receivingYards, receivingTouchdowns, points) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (*stats,))

db.commit() 
db.close()
driver.quit()