# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 22:18:37 2016

@author: Aidas
"""

"""
Create defensive and attack scaling factors for each team. If a lineup is not specified,
use a default (MostProbableLineup)

"""

#import os
#import math
import warnings
warnings.filterwarnings('ignore')

#from IPython.display import Image, HTML
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#import pymc as pm

import psycopg2
from pandas.io import sql

conn = psycopg2.connect(database="postgres", user="coxswain", password="Torpids2016", host="football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com", port="5432")
print ('Opened database successfully')
print("#####################################################################")

query1 = "SELECT * FROM PrabableLineUp"
probable_lineups = sql.read_sql(query1, con = conn)
query2 = "SELECT * FROM PlayerMatch"
player_stats = sql.read_sql(query2, con = conn)
query3 = "SELECT * FROM TeamMatch"
team_stats = sql.read_sql(query3, con = conn)
query4 = "SELECT * FROM Team"
teams = sql.read_sql(query4, con = conn)

print("#####################################################################")

num_teams = len(teams)
avg_ranking = player_stats.ranking.mean()

def find_team_attack_scales(lineups = probable_lineups):
    team_attack_scales = [None] *num_teams
    for i in range(num_teams):
        lineup_list = probable_lineups[probable_lineups.teamid == i][3:13]
        team_attack_scales[i] = team_attack_scale(i, lineup_list)
    return team_attack_scales
    
def find_team_defense_scales(lineups = probable_lineups):
    team_defense_scales = [None] *num_teams
    for i in range(num_teams):
        lineup_list = probable_lineups[probable_lineups.teamid == i][3:13]
        team_defense_scales[i] = team_defense_scale(i, lineup_list)
    return team_defense_scales
    
def find_team_ranking_scales(lineups = probable_lineups):
    team_ranking_scales = [None] *num_teams
    for i in range(num_teams):
        lineup_list = probable_lineups[probable_lineups.teamid == i][3:13]
        team_ranking_scales[i] = team_ranking_scale(i, lineup_list)
    return team_ranking_scales
    
#TODO: fix team scalings
   
#line_up is a list of player_id's
def team_attack_scale(team_id, lineup):
    total_scale = 0
    for player_id in lineup:
        player_contribution = player_attack_contribution(player_id)
        total_scale = total_scale + player_contribution
    return total_scale/team_attack_contribution(team_id)
    
def team_defense_scale(team_id, lineup):
    total_scale = 0
    for player_id in lineup:
        player_contribution = player_defense_contribution(player_id)
        total_scale = total_scale + player_contribution
    return total_scale/team_defense_contribution(team_id)
  
def team_ranking_scale(team_id, lineup):
    total_scale = 0
    team_ranking = player_stats[player_stats.teamid == team_id].ranking.mean()
    for player_id in lineup:
        player_contribution = player_ranking_contribution(player_id)
        total_scale = total_scale + player_contribution
    return total_scale/team_ranking


print(player_stats.dtypes)
print(player_stats.describe)
     
def player_attack_contribution(player_id):
    stats = player_stats[player_stats.playerid == player_id]
    mins_played = stats.minutes.sum()
    if(mins_played < 90):
        mins_played = 90
    goals = stats.goals.sum()
    scorring_att = stats.scoringatt.sum()
    on_target = stats.ontarget.sum()
    through_ball = stats.throughball.sum()
    att_assist = stats.attassist.sum()
    successful_passes = stats.successfulpasses.sum()
    return (goals/(mins_played * 1.4) * 0.4513 +
            scorring_att/(mins_played * 14.11) * 0.045 +
            on_target/(mins_played * 4.63) * 0.135 +
            through_ball/(mins_played * 1.7) * 0.283 +
            att_assist/(mins_played * 10.52) * 0.084 +
            successful_passes/(mins_played * 367) * 0.0017)
      
def player_defense_contribution(player_id):
    stats = player_stats[player_stats.playerid == player_id]
    mins_played = stats.minutes.sum()
    if(mins_played < 90):
        mins_played = 90
    tackles = stats.tackles.sum()
    clearances = stats.clearances.sum()
    interceptions = stats.interceptions.sum()
    duels_won = stats.duels_won.sum()
    return (tackles/(mins_played * 18.39) * 0.319 +
            clearances/(mins_played * 30.99) * 0.19 +
            interceptions/(mins_played * 15.77) * 0.373 +
            duels_won/(mins_played * 49.69) * 0.118)
      
def player_ranking_contribution(player_id):
    stats = player_stats[player_stats.playerid == player_id]
    rank_mean = stats.ranking.mean()
    return rank_mean/avg_ranking
    
def team_attack_contribution(team_id):
    stats = player_stats[player_stats.teamid == team_id]
    mins_played = stats.minutes.sum()
    if(mins_played < 90):
        mins_played = 90
    goals = stats.goals.sum()
    scorring_att = stats.scoringatt.sum()
    on_target = stats.ontarget.sum()
    through_ball = stats.throughball.sum()
    att_assist = stats.attassist.sum()
    successful_passes = stats.successfulpasses.sum()
    return (goals/(mins_played * 1.4) * 0.4513 +
            scorring_att/(mins_played * 14.11) * 0.045 +
            on_target/(mins_played * 4.63) * 0.135 +
            through_ball/(mins_played * 1.7) * 0.283 +
            att_assist/(mins_played * 10.52) * 0.084 +
            successful_passes/(mins_played * 367) * 0.0017)
      
def team_defense_contribution(team_id):
    stats = player_stats[player_stats.teamid == team_id]
    mins_played = stats.minutes.sum()
    if(mins_played < 90):
        mins_played = 90
    tackles = stats.tackles.sum()
    clearances = stats.clearances.sum()
    interceptions = stats.interceptions.sum()
    duels_won = stats.duels_won.sum()
    return (tackles/(mins_played * 18.39) * 0.319 +
            clearances/(mins_played * 30.99) * 0.19 +
            interceptions/(mins_played * 15.77) * 0.373 +
            duels_won/(mins_played * 49.69) * 0.118)
 


     