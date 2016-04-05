# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 19:23:09 2016

@author: Aidas
"""

# Uselful link:
# http://bigdataexaminer.com/uncategorized/how-to-run-linear-regression-in-python-scikit-learn/

import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
import psycopg2
from pandas.io import sql

conn = psycopg2.connect(database="postgres", user="coxswain", password="Torpids2016", host="football.c7v4rmvelqsx.eu-west-1.rds.amazonaws.com", port="5432")
print ('Opened database successfully')
print("#####################################################################")

query1 = "SELECT * FROM Players"
data = sql.read_sql(query1, con = conn)
X = data.drop('Value', axis = 1)

X_train, X_test, Y_train, Y_test = sklearn.cross_validation.train_test_split(
    X, data.value, test_size = 0.33, random_state = 5)

lm = stats.LinearRegression()

lm.fit(X_train, Y_train)
pred_train = lm.predict(X_train)
pred_test = lm.precict(X_test)

print("Fit a model X_train, and calculate MSE with Y_train:")
mseTrain = np.mean((Y_train - lm.predict(X_train)) ** 2)
print("Fit a model X_train, and calculate MSE with X_test, Y_test:")
mseTest = np.mean((Y_test - lm.predict(X_test)) ** 2)

plt.scatter(Y_train, pred_train)
plt.scatter(Y_test, pred_test)
plt.xlabel("Values: $Y_i$")
plt.ylabel("Predicted values: $Y_i$")
plt.title("Values vs Predicted Values: $Y_i$ vs $\hat{Y}_i$")
plt.show()


