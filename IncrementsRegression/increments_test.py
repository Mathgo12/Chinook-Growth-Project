import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#  Data Preprocessing
os.chdir('/Chinook-Salmon-Research-Project')
folderpath = "data/"
increments_fall_age_files = []
for file in os.listdir(folderpath):
    if 'increments' in file and "fall_age" in file:
        file_df = pd.read_csv(folderpath+file)
        file_df = file_df.drop("Unnamed: 0", axis=1)
        file_df["Group"] = file[0:-4]     #  filename without '.csv'
        increments_fall_age_files.append(file_df)

# Adding all data to one dataframe. Allows for subsetting of
# necessary data
increments_fall_age_df = pd.concat([df for df in increments_fall_age_files],axis=0)

X_ifa_full = increments_fall_age_df.loc[:, increments_fall_age_df.columns!='length'].drop("Group", axis=1).values
y_ifa_full = increments_fall_age_df.length.values

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer

columnTransformer = ColumnTransformer([('encoder', OneHotEncoder(), [1])], remainder='passthrough')
X_ifa_full = columnTransformer.fit_transform(X_ifa_full)
X_ifa_train, X_ifa_test, y_ifa_train, y_ifa_test = train_test_split(X_ifa_full, y_ifa_full, test_size=0.05, random_state=34)

from sklearn.ensemble import RandomForestRegressor

trees= 100
max_samples = 1000         #Number of training data points used for each bootstrapped sample
min_samples_split = 2      #Min number of data points to split each tree at each node
oob_score = True
min_impurity_decrease = 0.1

regressor_ifa = RandomForestRegressor(n_estimators=trees, oob_score=oob_score, min_impurity_decrease=min_impurity_decrease)
regressor_ifa.fit(X_ifa_train, y_ifa_train)
