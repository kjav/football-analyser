# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 19:25:21 2016

@author: Aidas
"""

import math
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import pymc as pm

import psycopg2
from pandas.io import sql

conn = psycopg2.connect(database="postgres", user="coxswain", password="Torpids2016", host="football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com", port="5432")
print ('Opened database successfully')
print("#####################################################################")

query = "SELECT * FROM TeamMatch"
stats = sql.read_sql(query, con = conn)
print("Initial results table")
print(stats.head())
print("#####################################################################")

