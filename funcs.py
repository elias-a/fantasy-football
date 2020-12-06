import numpy as np
import matplotlib.pyplot as plt
from helpers import scrape
from bs4 import BeautifulSoup

from config import LEAGUE_ID, UPDATE

# Return dictionary of team IDs and names
def GetTeams():
  url = 'https://fantasy.nfl.com/league/' + LEAGUE_ID
  filename = 'data/teams.txt'

  # Scrape fresh data, if desired
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

# Return dictionary of team IDs and manager names
def GetManagers():
  url = 'https://fantasy.nfl.com/league/' + LEAGUE_ID + '/owners'
  filename = 'data/managers.txt'

  # Scrape fresh data, if desired
  if UPDATE:
    scrape(url, filename)

  f = open(filename, 'r')

  txt = f.read()
  html = BeautifulSoup(txt, 'html.parser')

  data = html.find_all('a', { 'class': 'teamName' })

  managers = {}
  for d in data:
    manager = d.parent.parent.nextSibling.text
    managers[d['class'][1][-1]] = manager

  f.close()

  return managers

# Get weekly scores for each team
def GetScores():
  scores = {}
  
  # First 12 weeks
  for week in range(12):
    week = str(week + 1)
    url = 'https://fantasy.nfl.com/league/' + LEAGUE_ID + '/team/3/gamecenter?week=' + week
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

def PlotWeeklyScores(all_scores, teams):
  
  # Bar chart of team scores by week
  plt.figure()

  for week in range(1, 13):
    team_ids = []
    team_names = []
    scores = []

    for team in teams.keys():
      team_ids.append(team)
      team_names.append(teams[team])
      scores.append(all_scores[str(week)][team])

    plt.subplot(4, 3, week)
    plt.bar(team_ids, scores)
    
  plt.show()

def PlotTeamScores(all_scores, teams):
  plt.figure()

  for index, team in enumerate(teams):
    scores = [all_scores[week][team] for week in all_scores]
    
    plt.subplot(5, 2, index + 1)
    plt.plot(range(1, 13), scores)

  plt.show()

def PlotSummaryStats(all_scores, teams):
  fig = plt.figure()

  team_ids = []
  average = []
  std = []
  maximum = []
  minimum = []
  for team in teams:
    team_ids.append(team)
    scores = [all_scores[week][team] for week in all_scores]
    
    average.append(np.mean(scores))
    std.append(np.std(scores))
    maximum.append(np.max(scores))
    minimum.append(np.min(scores))
  
  ax1 = fig.add_subplot(2, 2, 1)
  ax1.bar(team_ids, average)
  ax1.title.set_text('Average Score')

  ax2 = fig.add_subplot(2, 2, 2)
  ax2.bar(team_ids, std)
  ax2.title.set_text('Standard Deviation of Average Score')

  ax3 = fig.add_subplot(2, 2, 3)
  ax3.bar(team_ids, maximum)
  ax3.title.set_text('Maximum Score')

  ax4 = fig.add_subplot(2, 2, 4)
  ax4.bar(team_ids, minimum)
  ax4.title.set_text('Minimum Score')

  plt.show()

  std_average = np.std(average)
  std_max = np.std(maximum)
  std_min = np.std(minimum)