# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 10:51:51 2016

@author: Aidas
"""

#import os
import math
import warnings
warnings.filterwarnings('ignore')

#from IPython.display import Image, HTML
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import pymc as pm

import psycopg2
from pandas.io import sql

import player_contribution as pc

conn = psycopg2.connect(database="postgres", user="coxswain", password="Torpids2016", host="football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com", port="5432")
print ('Opened database successfully')
print("#####################################################################")

query = "SELECT * FROM Match"
results = sql.read_sql(query, con = conn)
query1 = "SELECT * FROM PrabableLineUp"
probable_lineups = sql.read_sql(query1, con = conn)
print("Initial results table")
print(results.head())
print("#####################################################################")

teams = results.hometeam.unique()
teams = pd.DataFrame(teams, columns=['team'])
teams['i'] = teams.index
print("Teams")
print(teams.head())
print("#####################################################################")

results = pd.merge(results, teams, left_on = 'hometeam', right_on = 'team', how = 'left')
results = results.rename(columns = {'i': 'i_home'}).drop('team', 1)
results = pd.merge(results, teams, left_on = 'awayteam', right_on = 'team', how = 'left')
results = results.rename(columns = {'i': 'i_away'}).drop('team',1)
print("Merged table")
print (results.head())
print("#####################################################################")

observed_home_goals = results.homegoals.values
observed_away_goals = results.awaygoals.values
home_team = results.i_home.values
away_team = results.i_away.values
num_teams = len(results.i_home.unique())
num_games = len(home_team)

lineups = probable_lineups.copy()
#lineups is dataFrame of the same form as ProbableLineup table in db
def set_up_lineup(team_id, lineup):
    for i in range(11):
        lineups.teamid[i] = lineup[i + 3]


#Initial values for att and def parameters
g = results.groupby('i_away')
att_starting_points = np.log(g.awaygoals.mean())
g = results.groupby('i_home')
def_starting_points = -np.log(g.awaygoals.mean())
    
# Values reported in Rue & Salvesen model
homeGoalAvg = 0.395
awayGoalAvg = 0.098
att_scales = pc.find_team_attack_scales(lineups)
def_scales = pc.find_team_defense_scales(lineups)
#hyperpriors

#home = pm.Normal('home', 0, .0001, value=0)
tau_att = pm.Gamma('tau_att', .1, .1, value=10)
tau_def = pm.Gamma('tau_def', .1, .1, value=10)
intercept = pm.Normal('intercept', 0, .0001, value=0)

#team-specific parameters
atts_star = pm.Normal("atts_star", 
                        mu=0, 
                        tau=tau_att, 
                        size=num_teams, 
                        value=att_starting_points.values)
defs_star = pm.Normal("defs_star", 
                        mu=0, 
                        tau=tau_def, 
                        size=num_teams, 
                        value=def_starting_points.values) 

@pm.deterministic
def atts_star_scaled(atts_star=atts_star):
    return atts_star + np.log(att_scales)

@pm.deterministic
def defs_star_scaled(defs_star=defs_star):
    return defs_star + np.log(def_scales)

# trick to code the sum to zero contraint
@pm.deterministic
def atts(atts_star=atts_star):
    atts = atts_star_scaled.copy()
    atts = atts - np.mean(atts_star_scaled)
    return atts

@pm.deterministic
def defs(defs_star=defs_star):
    defs = defs_star_scaled.copy()
    defs = defs - np.mean(defs_star_scaled)
    return defs

@pm.deterministic
def home_theta(home_team=home_team, 
               away_team=away_team, 
               homeGoalAvg=homeGoalAvg, 
               atts=atts, 
               defs=defs, 
               intercept=intercept): 
    return np.exp(intercept + 
                  homeGoalAvg + 
                  atts[home_team] + 
                  defs[away_team])
  
@pm.deterministic
def away_theta(home_team=home_team, 
               away_team=away_team, 
               awayGoalAvg=awayGoalAvg, 
               atts=atts, 
               defs=defs, 
               intercept=intercept): 
    return np.exp(intercept + 
                  awayGoalAvg +
                  atts[away_team] + 
                  defs[home_team])   


home_goals = pm.Poisson('home_goals', 
                          mu=home_theta, 
                          value=observed_home_goals, 
                          observed=True)
away_goals = pm.Poisson('away_goals', 
                          mu=away_theta, 
                          value=observed_away_goals, 
                          observed=True)


model = pm.Model([intercept, tau_att, tau_def, 
                  home_theta, away_theta, 
                  atts_star, defs_star,
                  atts_star_scaled, defs_star_scaled, 
                  atts, defs, 
                  home_goals, away_goals])
              
mcmc = pm.MCMC(model)
map_ = pm.MAP( mcmc )
map_.fit()
mcmc.sample(200000, 40000, 20)

"""
##############################################
#Visualization:

pm.Matplot.plot(home)
pm.Matplot.plot(intercept)
pm.Matplot.plot(tau_att)
pm.Matplot.plot(tau_def)
pm.Matplot.plot(atts)

Embed = Image('atts.png')
print(Embed)


results_hpd = pd.DataFrame(atts.stats()['95% HPD interval'], 
                      columns=['hpd_low', 'hpd_high'], 
                      index=teams.team.values)
results_median = pd.DataFrame(atts.stats()['quantiles'][50], 
                         columns=['hpd_median'], 
                         index=teams.team.values)
results_hpd = results_hpd.join(results_median)
results_hpd['relative_lower'] = results_hpd.hpd_median - results_hpd.hpd_low
results_hpd['relative_upper'] = results_hpd.hpd_high - results_hpd.hpd_median
results_hpd = results_hpd.sort_index(by='hpd_median')
results_hpd = results_hpd.reset_index()
results_hpd['x'] = results_hpd.index + .5


fig, axs = plt.subplots(figsize=(10,4))
axs.errorbar(results_hpd.x, results_hpd.hpd_median, 
             yerr=(results_hpd[['relative_lower', 'relative_upper']].values).T, 
             fmt='o')
axs.set_title('HPD of Attack Strength, by Team')
axs.set_xlabel('Team')
axs.set_ylabel('Posterior Attack Strength')
_= axs.set_xticks(results_hpd.index + .5)
_= axs.set_xticklabels(results_hpd['index'].values, rotation=45)

"""

###################################################
#Simulations:

def simulate_season():
    """
    Simulate a season once, using one random draw from the mcmc chain. 
    """
    num_samples = atts.trace().shape[0]
    draw = np.random.randint(0, num_samples)
    atts_draw = pd.DataFrame({'att': atts.trace()[draw, :],})
    defs_draw = pd.DataFrame({'def': defs.trace()[draw, :],})
    #home_draw = home.trace()[draw]
    intercept_draw = intercept.trace()[draw]
    season = results.copy()
    season = pd.merge(season, atts_draw, left_on='i_home', right_index=True)
    season = pd.merge(season, defs_draw, left_on='i_home', right_index=True)
    season = season.rename(columns = {'att': 'att_home', 'def': 'def_home'})
    season = pd.merge(season, atts_draw, left_on='i_away', right_index=True)
    season = pd.merge(season, defs_draw, left_on='i_away', right_index=True)
    season = season.rename(columns = {'att': 'att_away', 'def': 'def_away'})
    #season['home'] = home_draw
    season['intercept'] = intercept_draw
    season['home_theta'] = season.apply(lambda x: math.exp(x['intercept'] + 
                                                           x['home'] + 
                                                           x['att_home'] + 
                                                           x['def_away']), axis=1)
    season['away_theta'] = season.apply(lambda x: math.exp(x['intercept'] + 
                                                           x['att_away'] + 
                                                           x['def_home']), axis=1)
    season['home_goals'] = season.apply(lambda x: np.random.poisson(x['home_theta']), axis=1)
    season['away_goals'] = season.apply(lambda x: np.random.poisson(x['away_theta']), axis=1)
    season['home_outcome'] = season.apply(lambda x: 'win' if x['home_goals'] > x['away_goals'] else 
                                                    'loss' if x['home_goals'] < x['away_goals'] else 'draw', axis=1)
    season['away_outcome'] = season.apply(lambda x: 'win' if x['home_goals'] < x['away_goals'] else 
                                                    'loss' if x['home_goals'] > x['away_goals'] else 'draw', axis=1)
    season = season.join(pd.get_dummies(season.home_outcome, prefix='home'))
    season = season.join(pd.get_dummies(season.away_outcome, prefix='away'))
    return season

def create_season_table(season):
    """
    Using a season dataframe output by simulate_season(), create a summary dataframe with wins, losses, goals for, etc.
    
    """
    g = season.groupby('i_home')    
    home = pd.DataFrame({'home_goals': g.home_goals.sum(),
                         'home_goals_against': g.away_goals.sum(),
                         'home_wins': g.home_win.sum(),
                         'home_draws': g.home_draw.sum(),
                         'home_losses': g.home_loss.sum()
                         })
    g = season.groupby('i_away')    
    away = pd.DataFrame({'away_goals': g.away_goals.sum(),
                         'away_goals_against': g.home_goals.sum(),
                         'away_wins': g.away_win.sum(),
                         'away_draws': g.away_draw.sum(),
                         'away_losses': g.away_loss.sum()
                         })
    results = home.join(away)
    results['wins'] = results.home_wins + results.away_wins
    results['draws'] = results.home_draws + results.away_draws
    results['losses'] = results.home_losses + results.away_losses
    results['points'] = results.wins * 3 + results.draws
    results['gf'] = results.home_goals + results.away_goals
    results['ga'] = results.home_goals_against + results.away_goals_against
    results['gd'] = results.gf - results.ga
    results = pd.merge(teams, results, left_on='i', right_index=True)
    results = results.sort_index(by='points', ascending=False)
    results = results.reset_index()
    results['position'] = results.index + 1
    results['champion'] = (results.position == 1).astype(int)
    results['qualified_for_CL'] = (results.position < 5).astype(int)
    results['relegated'] = (results.position > 17).astype(int)
    return results  
    
def simulate_seasons(n=100):
    resultss = []
    for i in range(n):
        s = simulate_season()
        t = create_season_table(s)
        t['iteration'] = i
        resultss.append(t)
    return pd.concat(resultss, ignore_index=True)

