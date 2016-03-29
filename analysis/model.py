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

# Small constatnt to acoid sampler getting stuck
C = 0.0001

#Scaling-specific parameter for beta distributions
S = 10

#Loss of memory effect for beta distributions
eps = 3
rho = 10

tau = pm.Gamma('tau', 10, 1)
precision = pm.Gamma('precision', 10, 0.1)

# Stupid initialization
# TODO CHANGE  IT
####################################################
noTeams = 20
noTimeslices = 38
noGames = 200

####################################################
unscaledattack = [[None]*noTeams for i in range(noTimeslices)]
unscaleddefense = [[None]*noTeams for i in range(noTimeslices)]
ascale = [[None]*noTeams for i in range(noTimeslices)]
dscale = [[None]*noTeams for i in range(noTimeslices)]

attack = [[None]*noTeams for i in range(noTimeslices)]
defense = [[None]*noTeams for i in range(noTimeslices)]
passSuccess = [[None]*noTeams for i in range(noTimeslices)]
aerialSuccess = [[None]*noTeams for i in range(noTimeslices)]
contestSuccess = [[None]*noTeams for i in range(noTimeslices)]
possession = [[None]*noTeams for i in range(noTimeslices)]
attempts = [[None]*noTeams for i in range(noTimeslices)]
saves = [[None]*noTeams for i in range(noTimeslices)]
motion = [[None]*noTeams for i in range(noTimeslices)]
days = [[None]*noTeams for i in range(noTimeslices)]
betaScale = [[None]*noTeams for i in range(noTimeslices)]

playSkillDiff = [None] * noGames
team = [[None]*noGames for i in range(2)]
timeslice = [[None]*noGames for i in range(2)]
hAttSkill = [None] * noGames
hDefSkill = [None] * noGames
aAttSkill = [None] * noGames
aDefSkill = [None] * noGames
wHomeAtt = [None] * noGames
wHomeDef = [None] * noGames
wAwayAtt = [None] * noGames
wAwayDef = [None] * noGames
delta = [None] * noGames
homeLambda = [None] * noGames
awayLambda = [None] * noGames
goalsScored = [[None]*noGames for i in range(2)]


####################################################

# Loop though all teams and all timeslices
for t in range(0 ,noTeams):
    # Initial distribution of attack/defence strength
    unscaledattack[t, 1] = pm.Normal('unscaledattack_%t' % t, 0, precision)
    unscaleddefense[t, 1] = pm.Normal('unscaleddefence_%t' % t, 0, precision)

    attack[t, 1] = unscaledattack[t, 1]
    defense[t, 1] = unscaleddefense[t, 1]

    
    # Initial distribution of other skill parameters
    # Add C to avoid sampler getting stuck at inf
    #TODO look at truncating
    
    passSuccess[t,1] = pm.Beta('passSuccess_%t' % t, 0.7*S, 0.3*S)
    aerialSuccess[t,1] = pm.Beta('aerialSuccess_%t' % t, 0.5*S, 0.5*S)
    contestSuccess[t,1] = pm.Beta('contestSuccess_%t' % t, 0.5*S, 0.5*S)
    possession[t,1] = pm.Beta('possession_%t' % t, 0.5*S, 0.5*S)
    attempts[t,1] = pm.Beta('attempts_%t' % t, 0.5*S, 0.5*S)
    saves[t,1] = pm.Beta('saves_%t' % t, 0.7*S, 0.3*S)
    
    # Evolve the attack/defence strength over to,e with Brownian motion (Wiener process).
    
    # The parameters are normally distributed with mean equal to the parameter value of
    # the previous timeslice (round). Loss - of - memory effect provided by variance parameter.
    #Implements a custom scaling technique for beta-distribution to mimic Brownian motian
    
    for s in range(1, noTimeslices):
        motion[t,s] = (abs(days[t,s] - days[t, s-1]) / tau) * precision
        
        unscaledattack[t,s] = pm.Normal(unscaledattack[t, s-1], motion[t,s])
        
        unscaleddefense[t,s] = pm.Normal(unscaleddefense[t, s-1], motion[t,s])
        
        betaScale[t, s] = S - (abs(days[t,s] - days[t, s-1])) / rho
        
        passSuccess[t,s] = pm.Beta((passSuccess[t, s-1] + C) * betaScale[t,s],
                                  (1- passSuccess[t, s-1] + C) * betaScale[t,s])
                                  
        aerialSuccess[t,s] = pm.Beta((aerialSuccess[t, s-1] + C) * betaScale[t,s],
                                  (1- aerialSuccess[t, s-1] + C) * betaScale[t,s]) 
                                  
        contestSuccess[t,s] = pm.Beta((contestSuccess[t, s-1] + C) * betaScale[t,s],
                                  (1- contestSuccess[t, s-1] + C) * betaScale[t,s])
                                  
        possession[t,s] = pm.Beta((possession[t, s-1] + C) * betaScale[t,s],
                                  (1- possession[t, s-1] + C) * betaScale[t,s])
                                  
        attempts[t,s] = pm.Beta((attempts[t, s-1] + C) * betaScale[t,s],
                                  (1- attempts[t, s-1] + C) * betaScale[t,s])
        
        saves[t,s] = pm.Beta((saves[t, s-1] + C) * betaScale[t,s],
                                  (1- saves[t, s-1] + C) * betaScale[t,s])
    

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

# Scalers for limiting impact of att/def skill
attSkillScaler = pm.Uniform('attSkillScaler', 0, 0.25)
defSkillScaler = pm.Uniform('defSkillScaler', 0, 0.25)

# Loop through all games in correct order
for i in range(0, noGames):
    # Home team open play skill
    playSkillDiff[i] = (passSuccess[team[i, 1], timeslice[i,1]] -
                        passSuccess[team[i, 2], timeslice[i,2]] +
                        aerialSuccess[team[i, 1], timeslice[i,1]] -
                        aerialSuccess[team[i, 2], timeslice[i,2]] +
                        contestSuccess[team[i, 1], timeslice[i,1]] -
                        contestSuccess[team[i, 2], timeslice[i,2]] +
                        possession[team[i, 1], timeslice[i,1]] -
                        possession[team[i, 2], timeslice[i,2]]
                    )
                    
    # Home team attack - specific skill
    hAttSkill[i] = (playSkillDiff[i] +
                    attempts[team[i, 1], timeslice[i, 1]] -
                    saves[team[i, 2], timeslice[i, 2]]) / 5
    
    # Home team defense - specific skill
    hDefSkill[i] = (playSkillDiff[i] +
                    saves[team[i, 1], timeslice[i, 1]] -
                    attempts[team[i, 2], timeslice[i, 2]]) / 5
    
    # Away team attack specific skill
    aAttSkill[i] = 0 - hDefSkill[i]
    
    # Away team defense specific skill
    aDefSkill[i] = 0 - hAttSkill[i]
    
    # Attack/defense node mutators
    wHomeAtt[i] = (hAttSkill[i] * attSkillScaler) + attack[team[i, 1], timeslice[i, 1]]
    wHomeDef[i] = (hDefSkill[i] * defSkillScaler) + defense[team[i, 1], timeslice[i, 1]]
    wAwayAtt[i] = (aAttSkill[i] * attSkillScaler) + attack[team[i, 2], timeslice[i, 2]]
    wAwayDef[i] = (aAttSkill[i] * defSkillScaler) + attack[team[i, 2], timeslice[i, 2]]

    # delta param for psychological effect of underestimating
    delta[i] = (wHomeAtt[i] + wHomeDef[i] -
                wAwayAtt[i] - wAwayDef[i]) /2
                
    # Home lambda parameter
    homeLambda[i] = pm.Exponential(homeGoalAvg + wHomeAtt[i] - wAwayDef[i] - gamma * delta[i])
    
    # Away lambda parameter
    awayLambda[i] = pm.Exponential(awayGoalAvg + wAwayAtt[i] - wHomeDef[i] + gamma * delta[i])
    
    
    goalsScored[i, 1] = pm.Poisson(homeLambda[i])
    goalsScored[i, 2] = pm.Poisson(awayLambda[i])
    

    

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

