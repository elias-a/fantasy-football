import os
import numpy as np
import matplotlib.pyplot as plt
from helpers import scrape, format_name, run_regression
from bs4 import BeautifulSoup

from config import LEAGUE_ID, UPDATE

# Return dictionary of team IDs and names
def GetTeams():
  url = 'https://fantasy.nfl.com/league/' + LEAGUE_ID
  filename = os.path.dirname(os.path.realpath(__file__)) + '/data/teams.txt'

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
  filename = os.path.dirname(os.path.realpath(__file__)) + '/data/managers.txt'

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
    filename = os.path.dirname(os.path.realpath(__file__)) + '/data/scores' + week + '.txt'

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

# Bar charts of team scores by week
def PlotWeeklyScores(all_scores, teams):
  fig = plt.figure()

  for week in range(1, 13):
    team_ids = []
    team_names = []
    scores = []

    for team in teams.keys():
      team_ids.append(team)
      team_names.append(format_name(teams[team]))
      scores.append(all_scores[str(week)][team])

    ax = fig.add_subplot(4, 3, week)
    ax.bar(team_names, scores)
    ax.title.set_text('Week ' + str(week))

  fig.tight_layout()
  plt.show()

# Line plots of scores by team
def PlotTeamScores(all_scores, teams):
  fig = plt.figure()

  for index, team in enumerate(teams):
    scores = [all_scores[week][team] for week in all_scores]
    
    ax = fig.add_subplot(5, 2, index + 1)
    ax.plot(range(1, 13), scores)
    ax.title.set_text(teams[team])

  fig.tight_layout()
  plt.show()

# Plot summary statistics of team scoring
def PlotSummaryStats(all_scores, teams):
  fig = plt.figure()

  team_names = []
  team_ids = []
  average = []
  std = []
  maximum = []
  minimum = []
  for team in teams:
    name = format_name(teams[team])
    team_names.append(name)
    team_ids.append(team)
    scores = [all_scores[week][team] for week in all_scores]
    
    average.append(np.mean(scores))
    std.append(np.std(scores))
    maximum.append(np.max(scores))
    minimum.append(np.min(scores))
  
  ax1 = fig.add_subplot(2, 2, 1)
  ax1.bar(team_names, average)
  ax1.title.set_text('Average Score')

  ax2 = fig.add_subplot(2, 2, 2)
  ax2.bar(team_names, std)
  ax2.title.set_text('Standard Deviation of Average Score')

  ax3 = fig.add_subplot(2, 2, 3)
  ax3.bar(team_names, maximum)
  ax3.title.set_text('Maximum Score')

  ax4 = fig.add_subplot(2, 2, 4)
  ax4.bar(team_names, minimum)
  ax4.title.set_text('Minimum Score')

  plt.show()

  std_average = np.std(average)
  std_max = np.std(maximum)
  std_min = np.std(minimum)

"""
Determine how much a team "explodes" compared to other teams,
in both magnitude and frequency.
"""
def CalcExplosiveness(weekly_scores, teams):
  team_names = []
  team_scores = []
  team_variation = []
  team_explosiveness = {}

  for team in teams:
    explosiveness = []
    explosion_factor = 0
    implosion_factor = 0

    scores = [weekly_scores[week][team] for week in weekly_scores]

    avg_score = np.mean(scores)
    std_avg_score = np.std(scores)
    
    upper_lim = avg_score + std_avg_score
    lower_lim = avg_score - std_avg_score
    explosions = [week for week in scores if week > upper_lim]
    implosions = [week for week in scores if week < lower_lim]

    for explosion in explosions:
      # Calculate percentage above average
      perc_above_avg = (explosion - avg_score) / avg_score
      explosion_factor += 100 * perc_above_avg

    for implosion in implosions:
      # Calculate percentage below average
      perc_below_avg = (avg_score - implosion) / avg_score
      implosion_factor += 100 * perc_below_avg

    combined_factor = explosion_factor + implosion_factor
    net_factor = explosion_factor - implosion_factor

    team_explosiveness[team] = [explosion_factor, implosion_factor, combined_factor, net_factor]

    team_names.append(format_name(teams[team]))
    team_scores.append(avg_score)
    team_variation.append(std_avg_score)

  fig = plt.figure() 
  ax = fig.add_subplot(1, 1, 1)
  ax.bar(team_names, team_scores, yerr=team_variation, capsize=10)
  ax.title.set_text('Average Points Scored')
  plt.show()

  return team_explosiveness

def GetRecords():
  url = 'https://fantasy.nfl.com/league/' + LEAGUE_ID
  filename = 'data/records.txt'

  # Scrape fresh data, if desired
  if UPDATE:
    scrape(url, filename)

  f = open(filename, 'r')

  txt = f.read()
  html = BeautifulSoup(txt, 'html.parser')

  data = html.find_all('td', { 'class': 'teamWinPct' })

  records = {}
  for d in data:
    records[d.parent['class'][0][-1]] = d.text

  f.close()

  return records

def AnalyzeExplosiveness(team_records, team_explosiveness):
  records = []
  explosions = []
  implosions = []
  combined = []
  net = []

  teams = {k: v for k, v in sorted(team_records.items(), key=lambda item: item[1])}

  for team in teams:
    record = team_records[team]
    explosiveness = team_explosiveness[team]

    records.append(float(record))
    explosions.append(explosiveness[0])
    implosions.append(explosiveness[1])
    combined.append(explosiveness[2])
    net.append(explosiveness[3])

  fig = plt.figure()

  records_list = np.arange(0, 1, 0.01)

  intercept, coef, R_sq = run_regression(records, explosions)
  explosions_list = intercept + coef * records_list

  ax1 = fig.add_subplot(2, 2, 1)
  ax1.scatter(records, explosions)
  ax1.plot(records_list, explosions_list)
  ax1.title.set_text('Explosions, R_sq=' + str(np.round(R_sq, 2)))

  intercept, coef, R_sq = run_regression(records, implosions)
  implosions_list = intercept + coef * records_list

  ax2 = fig.add_subplot(2, 2, 2)
  ax2.scatter(records, implosions)
  ax2.plot(records_list, implosions_list)
  ax2.title.set_text('Implosions, R_sq=' + str(np.round(R_sq, 2)))

  intercept, coef, R_sq = run_regression(records, combined)
  combined_list = intercept + coef * records_list

  ax3 = fig.add_subplot(2, 2, 3)
  ax3.scatter(records, combined)
  ax3.plot(records_list, combined_list)
  ax3.title.set_text('Combined (Explosions + Implosions), R_sq=' + str(np.round(R_sq, 2)))

  intercept, coef, R_sq = run_regression(records, net)
  net_list = intercept + coef * records_list

  ax4 = fig.add_subplot(2, 2, 4)
  ax4.scatter(records, net)
  ax4.plot(records_list, net_list)
  ax4.title.set_text('Net (Explosions - Implosions), R_sq=' + str(np.round(R_sq, 2)))

  plt.show()