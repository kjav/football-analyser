# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 10:19:39 2016

@author: Aidas
"""

import sys
import math
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import player_contribution as pc
import model as mod

prob_lineups = [None]*mod.num_teams
for i in range(1,mod.num_teams+1):
    prob_lineups[i-1] = list(mod.probable_lineups[mod.probable_lineups.teamid == i].values[0][2:13])

lineups = prob_lineups
#rtg_scales = []
def set_up_lineups(team_id, team_lineup):
    lineups[team_id - 1] = team_lineup

def simulate_game(home_team, away_team, rtg_scales):
    num_samples = mod.atts.trace().shape[0]
    draw = np.random.randint(0, num_samples)
    att_home_draw = mod.atts.trace()[draw, home_team]
    att_away_draw = mod.atts.trace()[draw, away_team]
    def_home_draw = mod.defs.trace()[draw, home_team]
    def_away_draw = mod.defs.trace()[draw, away_team]
    home_draw = mod.home.trace()[draw]
    intercept_draw = mod.intercept.trace()[draw]
    home_theta = rtg_scales[home_team]* (1/rtg_scales[away_team])* math.exp(intercept_draw + home_draw + att_home_draw + def_away_draw)
    away_theta = rtg_scales[away_team]* (1/rtg_scales[home_team])* math.exp(intercept_draw + att_away_draw + def_home_draw)
    home_goals = np.random.poisson(home_theta)
    away_goals = np.random.poisson(away_theta)
    return (home_goals, away_goals)

def simulate_games(home_team, away_team, rtg_scales, n):
    total_home = 0.0
    total_away = 0.0
    for i in range(n):
        (h, a) = simulate_game(home_team, away_team, rtg_scales)
        total_home += h
        total_away += a
    return (total_home/n, total_away/n)

def execute():
    while(True):
        lineups = prob_lineups
        home_team = int(sys.stdin.readline())
        away_team = int(sys.stdin.readline())
        home_lineup = [int(x) for x in sys.stdin.readline().split()]
        away_lineup = [int(x) for x in sys.stdin.readline().split()]
        set_up_lineups(home_team, home_lineup)
        set_up_lineups(away_team, away_lineup)
        #print("Lineups", lineups)
        rtg_scales = pc.find_team_rating_scales(lineups)
        #print("RKG", rtg_scales)
        (h, a) = simulate_games(home_team - 1, away_team - 1, rtg_scales, 100000)
        res = (h, a)
        s= str(res)
        print(s)
        #sys.stdout.write(s)
        
execute()
"""
ars_lineups = [None] * 5
ars_lineups[0] = [351, 320, 303, 168, 383, 260, 25, 3, 348, 334, 143]
ars_lineups[1] = [351, 320, 303, 168, 383, 260, 21, 3, 348, 334, 143]
ars_lineups[2] = [351, 320, 205, 168, 383, 260, 21, 3, 348, 334, 143]
ars_lineups[3] = [351, 320, 205, 168, 19, 294, 21, 3, 348, 334, 143]
ars_lineups[4] = [351, 334, 19, 348, 293, 205, 294, 413, 66, 310, 251]

for i in range(5):    
    set_up_lineups(2, ars_lineups[i])
    rtg_scales = pc.find_team_rating_scales(lineups)
    print("")
    print("Lineup: ", i)
    print("Arsenal scaling factor", rtg_scales[1])
    for i in range(20):
        opp = list(mod.teams[mod.teams.id == (i+1)].values[0])[1]
        print("Opponent team: ", opp)
        print(simulate_games(1,i, 100000))
        print(simulate_games(i,1, 100000))
    print("")
    
"""    
"""
351 320 205 168 383 260 21 3 348 334 143
242 439 366 191 100 278 363 327 196 395 105
"""
