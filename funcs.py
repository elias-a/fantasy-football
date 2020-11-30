from helpers import scrape
from bs4 import BeautifulSoup

from config import league_id

UPDATE = True

# Return dictionary of team IDs and names
def GetTeams():
  url = 'https://fantasy.nfl.com/league/' + league_id
  filename = 'data/teams.txt'

  if UPDATE:
    scrape(url, filename)

  f = open(filename, 'r')

  txt = f.read()
  html = BeautifulSoup(txt, 'html.parser')

  data = html.find_all('a', { 'class': 'teamName' })

  teams = {}
  for d in data:
    teams[d['class'][1][-1]] = d.text

  f.close()

  return teams

# Get weekly scores for each team
def GetScores():
  scores = {}
  
  # First 11 weeks
  for week in range(11):
    week = str(week + 1)
    url = 'https://fantasy.nfl.com/league/' + league_id + '/team/3/gamecenter?week=' + week
    filename = 'data/scores' + week + '.txt'

    # Scrape fresh data, if desired
    if UPDATE: 
      scrape(url, filename)

    f = open(filename, 'r')

    txt = f.read()
    html = BeautifulSoup(txt, 'html.parser')

    totals = html.find_all('span', { 'class': 'teamTotal' })

    week_scores = {}
    for t in totals:
      team_id = t['class'][1][-1]
      week_scores[team_id] = float(t.text)

    scores[week] = week_scores

    f.close()

  return scores