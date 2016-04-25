import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd

import pymc as pm

import psycopg2
from pandas.io import sql

conn = psycopg2.connect(database="postgres", user="coxswain", password="Torpids2016", host="football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com", port="5432")
#print ('Opened database successfully')
#print("#####################################################################")

query_matches = "SELECT * FROM Match"
matches = sql.read_sql(query_matches, con = conn)
query_lineups = "SELECT * FROM ProbableLineUp"
probable_lineups = sql.read_sql(query_lineups, con = conn)
query_results = "SELECT * FROM Result"
results = sql.read_sql(query_results, con = conn)
query_teams = "SELECT * FROM Team"
teams = sql.read_sql(query_teams, con = conn)
#print("Teams")
#print(teams.head())
#print("Initial matches table")
matches = pd.merge(matches,results, left_on = 'result', right_on = 'id', how = 'left')
matches = matches.rename(columns = {'id_x': 'id'}).drop('id_y', 1).drop('result', 1).drop('stage', 1).drop('the_date', 1)
matches = matches.rename(columns = {'home_team': 'i_home'})
matches = matches.rename(columns = {'away_team': 'i_away'})
#print(matches.head())
#print("#####################################################################")

teams['i'] = teams.index
matches['i_home'] = matches.apply(lambda x: (x['i_home'] - 1), axis=1)
matches['i_away'] = matches.apply(lambda x: (x['i_away'] - 1), axis=1)


matches = pd.merge(matches, teams, left_on = 'i_home', right_on = 'i', how = 'left')
matches = matches.rename(columns = {'name': 'home_team'}).drop('i', 1).drop('id_y', 1)
matches = pd.merge(matches, teams, left_on = 'i_away', right_on = 'i', how = 'left')
matches = matches.rename(columns = {'name': 'away_team'}).drop('i',1).drop('id', 1)
matches = matches.rename(columns = {'id_x': 'id'})
print("Merged table")
print (matches.head())
print(teams)
print("#####################################################################")

observed_home_goals = matches.home_goals.values
observed_away_goals = matches.away_goals.values
home_team = matches.i_home.values
away_team = matches.i_away.values
num_teams = len(matches.i_home.unique())
num_games = len(home_team)

#Initial values for att and def parameters
g = matches.groupby('i_away')
att_starting_points = np.log(g.away_goals.mean())
g = matches.groupby('i_home')
def_starting_points = -np.log(g.away_goals.mean())

home = pm.Normal('home', 0, .0001, value=0)
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

# trick to code the sum to zero contraint
@pm.deterministic
def atts(atts_star=atts_star):
    atts = atts_star.copy()
    atts = atts - np.mean(atts_star)
    return atts

@pm.deterministic
def defs(defs_star=defs_star):
    defs = defs_star.copy()
    defs = defs - np.mean(defs_star)
    return defs

@pm.deterministic
def home_theta(home_team=home_team, 
               away_team=away_team, 
               home = home, 
               atts=atts, 
               defs=defs, 
               intercept=intercept): 
    return np.exp(intercept + 
                  home + 
                  atts[home_team] + 
                  defs[away_team])
  
@pm.deterministic
def away_theta(home_team=home_team, 
               away_team=away_team, 
               home = home, 
               atts=atts, 
               defs=defs, 
               intercept=intercept): 
    return np.exp(intercept + 
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

mcmc = pm.MCMC([home, intercept, tau_att, tau_def, 
                  home_theta, away_theta, 
                  atts_star, defs_star,
                  atts, defs, 
                  home_goals, away_goals])
              
map_ = pm.MAP( mcmc )
map_.fit()
mcmc.sample(200000, 100000, 20)
