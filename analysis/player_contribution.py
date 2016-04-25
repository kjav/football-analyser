# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 22:18:37 2016

@author: Aidas
"""

import warnings
warnings.filterwarnings('ignore')
import psycopg2
from pandas.io import sql

conn = psycopg2.connect(database="postgres", user="coxswain", password="Torpids2016", host="football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com", port="5432")
#print ('Opened database successfully')
#print("#####################################################################")

query1 = "SELECT * FROM ProbableLineUp"
probable_lineups = sql.read_sql(query1, con = conn)
query2 = "SELECT * FROM Player_Match"
player_stats = sql.read_sql(query2, con = conn)
query3 = "SELECT * FROM Team_Match"
team_stats = sql.read_sql(query3, con = conn)
query4 = "SELECT * FROM Team"
teams = sql.read_sql(query4, con = conn)
conn.close() 
#print("#####################################################################")

num_teams = len(teams)
avg_rating = player_stats.rating.mean()

lineup_list = [None]*num_teams
for i in range(1,num_teams+1):
    lineup_list[i-1] = list(probable_lineups[probable_lineups.teamid == i].values[0][2:13])


def set_up_lineups(team_id, team_lineup):
    lineup_list[team_id - 1] = team_lineup
    
    
def find_team_rating_scales(lineup_list):
    team_rating_scales = [None] *num_teams
    for i in range(num_teams):
        team_rating_scales[i] = team_rating_scale(i+1, lineup_list[i])
    return team_rating_scales
    

def team_rating_scale(team_id, lineup):
    total_scale = 0
    team_rating = 0
    prob = list(probable_lineups[probable_lineups.teamid == team_id].values[0][2:13])
    for pl_id in prob:
        team_rating = team_rating + player_rating_contribution(pl_id)**7
    team_rating = team_rating/11
    #team_rating = team_stats[team_stats.team == team_id].rating.mean()**7
    for player_id in lineup:
        player_contribution = player_rating_contribution(player_id)**7
        total_scale = total_scale + player_contribution
    
    return total_scale/(team_rating*11)

      
def player_rating_contribution(player_id):
    stats = player_stats[player_stats.playerid == player_id]
    rank_mean = stats.rating.mean()
    return rank_mean
