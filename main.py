from funcs import GetTeams, GetScores, PlotScores

# Get dictionary of team IDs and names
teams_dict = GetTeams()

# Get weekly scores for each team
scores = GetScores()

PlotScores(scores, teams_dict)