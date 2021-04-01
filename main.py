import sys
import funcs
from helpers import to_js

request = sys.argv[1]

if request == 'teams': 
    # Get dictionary of team IDs and names. 
    teams_dict = funcs.GetTeams()
    to_js(teams_dict)
elif request == 'managers':
    # Get dictionary of team IDs and manager names. 
    managers_dict = funcs.GetManagers()
    to_js(managers_dict)
elif request == 'weekly_scores':
    # Get weekly scores for each team. 
    scores = funcs.GetScores() 
    to_js(scores)

# Plot bar charts of team scores each week
#funcs.PlotWeeklyScores(scores, managers_dict)

# Plot line plots of scores by team
#funcs.PlotTeamScores(scores, managers_dict)

# Plot summary statistics of team scoring
#funcs.PlotSummaryStats(scores, managers_dict)

# Compute the Explosiveness Factor for each team
#explosiveness = funcs.CalcExplosiveness(scores, managers_dict)

# Get records for each team
#records = funcs.GetRecords()

#funcs.AnalyzeExplosiveness(records, explosiveness)