import pandas as pd
import numpy as np
import sklearn as sk
import matplotlib.pyplot as plt

data_COWL_fall = pd.read_csv("legacy_data/Regression Data/regression_data_COWL_fall.csv")

# prep data for random forest
data_rf = data_COWL_fall.drop(columns=['Unnamed: 0', 'brood_year'], axis=1)  # Release age and Release length are highly correlated

# drop unneeded columns
data_rf = data_rf.drop(['gear'], axis=1)

# filter out fisheries greater tha 60
data_rf = data_rf[data_rf.fishery < 60]
runs_nms = []
fishery_nms = []
age_nms = []
for ind, row in data_rf.iterrows():
    # convert ages to strings
    age_nms.append(str(row['age']))
    # convert run names
    if row['run'] == 3:
        runs_nms.append("fall")
    if row['run'] == 1:
        runs_nms.append("spring")
    if row['run'] == 2:
        runs_nms.append("summer")
    if row['run'] == 8:
        runs_nms.append("late_fall")

    # convert fishery
    if row['fishery'] > 9 and row['fishery'] < 20:
        fishery_nms.append("Troll")
    if row['fishery'] > 19 and row['fishery'] < 30:
        fishery_nms.append("Net")
    if row['fishery'] > 29 and row['fishery'] < 40:
        fishery_nms.append("Tribal")
    if row['fishery'] > 39 and row['fishery'] < 50:
        fishery_nms.append("Sport")
    if row['fishery'] > 49 and row['fishery'] < 60:
        fishery_nms.append("Escapement")

# add categorical variables back in
data_rf.run = runs_nms
data_rf.fishery = fishery_nms
data_rf.age = age_nms

# convert categorical variables to one-hot encoding
data_rf = pd.get_dummies(data_rf)

# data_rf.head(30)
y = data_rf.length
x = data_rf.loc[:, data_rf.columns != 'length'].values
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(n_estimators=1000, random_state=42)
# Train the model on training data

# mforestaking a feature importance plot 
feature_list = data_rf.columns[1:50]

# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key=lambda x: x[1], reverse=True)
# Print out the feature and importances 
print(['Variable: {:20} Importance: {}'.format(*pair) for pair in feature_importances])
