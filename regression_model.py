import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn as sk

path = "legacy_data/Regression Data/regression_data.csv"
# prep data for random forest
data_rf = pd.read_csv(path)
data_rf = data_rf.drop(columns=['Unnamed: 0', 'year', 'release_age'], axis=1)      #Release age and Release length are highly correlated


# drop unneeded columns
data_rf = data_rf.drop(['gear'], axis=1 )


# filter out fisheries greater tha 60 
data_rf = data_rf[data_rf.fishery < 60]
runs_nms = []
fishery_nms = []
age_nms = []
for ind, row in data_rf.iterrows():
  # convert ages to strings
  age_nms.append(str(row['age']))
  # convert run names 
  if row['run']  == 3:
    runs_nms.append("fall")
  if row['run']  == 1:
    runs_nms.append("spring")
  if row['run']  == 2:
    runs_nms.append("summer")
  if row['run']  == 8:
    runs_nms.append("late_fall")

  # convert fishery 
  if 9 < row['fishery'] < 20:
    fishery_nms.append("Troll")
  if 19 < row['fishery'] < 30:
    fishery_nms.append("Net")
  if 29 < row['fishery'] < 40:
    fishery_nms.append("Tribal")
  if 39 < row['fishery'] < 50:
    fishery_nms.append("Sport")
  if 49 < row['fishery'] < 60:
    fishery_nms.append("Escapement")


# add categorical variables back in 
data_rf.run = runs_nms
data_rf.fishery = fishery_nms
data_rf.age = age_nms

# convert categorical variables to one-hot encoding 
data_rf = pd.get_dummies(data_rf)

print(data_rf.shape)

#age 4, all lags
subset_age4 = data_rf.loc[data_rf.age_4==1].drop(['age_3','age_5'], axis=1)

#Split Data- training and testing sets
x_train2, x_test2, y_train2, y_test2 = sk.model_selection.train_test_split(subset_age4.loc[:, subset_age4.columns!='length'].values, subset_age4['length'].values, test_size = 0.2, random_state = 10)

#Standardization
scaler = sk.preprocessing.StandardScaler()

x_train2[:, :24] = scaler.fit_transform(x_train2[:, :24])
x_test2[:, :24] = scaler.transform(x_test2[:, :24])


climate_age4_data = subset_age4.iloc[:, 3:24].values
x_train_clim, x_test_clim, y_train_clim, y_test_clim = sk.model_selection.train_test_split(climate_age4_data, subset_age4['length'].values, test_size = 0.2, random_state=23)

#Data Distribution Visualization

fig, ax = plt.subplots(1, 1, figsize =(10, 7), tight_layout = True)
ax.hist(subset_age4.iloc[:, 1], bins=100)
ax.set_xlabel('Length')
ax.set_ylabel('Frequency')
ax.grid()

# subset_age4.iloc[:, :24].hist(bins=10, figsize=(40,30))  #plot feature frequencies
# plt.show()
features_skew = subset_age4.iloc[:, :24].skew().sort_values(ascending=False)  #Feature Skewness

#Feature Correlation with Pearson's r (Linear)
feature_rsquared = {}
for i in range(0,24):
  feature = subset_age4.iloc[:, i]
  length_y = subset_age4.loc[:, 'length']
  feature_rsquared[feature.name] = np.corrcoef(feature, length_y)  #Pearson's r, linear correlation
brood_year_v_length = feature_rsquared['brood_year']

trees= 500
max_samples = 1000         #Number of training data points used for each bootstrapped sample
min_samples_split = 2      #Min number of data points to split each tree at each node
oob_score = True
min_impurity_decrease = 0.1

rf = sk.ensemble.RandomForestRegressor(n_estimators=trees, oob_score = oob_score)
rf.fit(x_train2, y_train2)
rf.score(x_train2, y_train2)  #Computes R_squared

#pprint(rf.get_params())
print('OOB Score ' + str(rf.oob_score_))

#Randomized Search CV
from sklearn.model_selection import RandomizedSearchCV

param_grid = [
    {'n_estimators':np.arange(0,1000,50), 'max_features':np.arange()}
]


#Climate Data
trees= 500
max_samples = 1000         #Number of training data points used for each bootstrapped sample
min_samples_split = 2      #Min number of data points to split each tree at each node
oob_score = True
min_impurity_decrease = 0.1

rf = sk.ensemble.RandomForestRegressor(n_estimators=trees, oob_score = oob_score)
rf.fit(x_train2, y_train2)
rf.score(x_train2, y_train2)  #Computes R_squared

#pprint(rf.get_params())
print('OOB Score ' + str(rf.oob_score_))


