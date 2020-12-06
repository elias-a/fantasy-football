import funcs

# Get dictionary of team IDs and names
teams_dict = funcs.GetTeams()

# Get dictionary of team IDs and manager names
managers_dict = funcs.GetManagers()

# Get weekly scores for each team
scores = funcs.GetScores()

# Plot bar charts of team scores each week
funcs.PlotWeeklyScores(scores, teams_dict)

# Plot line plots of scores by team
funcs.PlotTeamScores(scores, teams_dict)

# Plot summary statistics 
funcs.PlotSummaryStats(scores, managers_dict)