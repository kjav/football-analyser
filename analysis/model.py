# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 17:58:30 2016

@author: Aidas
"""

#TODO change pm.Normal parameters to precision instead of variance

"""
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
"""

import math
import pymc as pm

# Values reported in Rue & Salvesen model
homeGoalAvg = 0.395
awayGoalAvg = 0.098

tau = pm.Gamma('tau', 10, 1)
precision = pm.Gamma('precision', 10, 0.1)

# Data from website
####################################################

####################################################

# Stupid initialization
# TODO CHANGE  IT
####################################################
noTeams = 20
noTimeslices = 38
noGames = 200
obsRounds = 10

####################################################
unscaledattack = [[None]*noTeams for i in range(noTimeslices)]
unscaleddefense = [[None]*noTeams for i in range(noTimeslices)]
ascale = [[None]*noTeams for i in range(noTimeslices)]
dscale = [[None]*noTeams for i in range(noTimeslices)]


attack = [[None]*noTeams for i in range(noTimeslices)]
defense = [[None]*noTeams for i in range(noTimeslices)]
motion = [[None]*noTeams for i in range(noTimeslices)]
days = [[None]*noTeams for i in range(noTimeslices)]

team = [[None]*noGames for i in range(2)]
timeslice = [[None]*noGames for i in range(2)]
delta = [None] * noGames
homeLambda = [None] * noGames
awayLambda = [None] * noGames
goalsScored = [[None]*noGames for i in range(2)]


####################################################

### TODO: Change python lists to pymc arrays
# Loop though all teams and all timeslices
for t in range(0 ,noTeams):
    # Initial distribution of attack/defence strength
    unscaledattack[t, 1] = pm.Normal('unscaledattack%d' % t, 0, precision)
    unscaleddefense[t, 1] = pm.Normal('unscaleddefence%d' % t, 0, precision)

    attack[t, 1] = unscaledattack[t, 1]
    defense[t, 1] = unscaleddefense[t, 1]

    # Evolve the attack/defence strength over to,e with Brownian motion (Wiener process).
    
    # The parameters are normally distributed with mean equal to the parameter value of
    # the previous timeslice (round). Loss - of - memory effect provided by variance parameter.
    #Implements a custom scaling technique for beta-distribution to mimic Brownian motian
    
    for s in range(1, noTimeslices):
        motion[t,s] = (abs(days[t,s] - days[t, s-1]) / tau) * precision
        
        unscaledattack[t,s] = pm.Normal(unscaledattack[t, s-1], motion[t,s])
        
        unscaleddefense[t,s] = pm.Normal(unscaleddefense[t, s-1], motion[t,s])
        
        attack[t, s] = unscaledattack[t,s] + math.log(ascale[s, t])
        
        defense[t, s] = unscaleddefense[t,s] + math.log(dscale[s, t])
        
        
### Goal Model
########################################

# Params:
# attack[t,s] / defense[t,s] = attack/defense strength for team t at a given timeslice s
# team[i, 1] = home team in game i
# team[i, 2] = away team in game i
# timeslice[i, 1] = timeslice(round/games played so far) of home team in game i
# timeslice[i, 2] = timeslice(round/games played so far) of away team in game i
# goalsScored[i, 1] = goals scored by home tea in game i
# goalsScored[i, 2] = goals scored by away team in game i

gamma = pm.Uniform('gamma', 0, 0.1)

# Loop through all games in correct order
for i in range(0, noGames):

    # delta param for psychological effect of underestimating
    delta[i] = (attack[team[i, 1], timeslice[i, 1]] + 
                defense[team[i, 1], timeslice[i, 1]] -
                attack[team[i, 2], timeslice[i, 2]] -
                defense[team[i, 2], timeslice[i, 2]]) / 2

    # Home lambda parameter
    @pm.deterministic
    def homeLambda(i):
        return math.exp(homeGoalAvg + attack[team[i, 1], timeslice[i, 1]] - 
                            defense[team[i, 2], timeslice[i, 2]] - gamma * delta[i])
    
    # Away lambda parameter
    @pm.deterministic
    def awayLambda(i):
        return math.exp(awayGoalAvg + attack[team[i, 2], timeslice[i, 2]] - 
                defense[team[i, 1], timeslice[i, 1]] + gamma * delta[i])    
    
    
    goalsScored[i, 1] = pm.Poisson(homeLambda[i])
    goalsScored[i, 2] = pm.Poisson(awayLambda[i])
    
    
    
    
    
    
    
    
    
    
    
    

