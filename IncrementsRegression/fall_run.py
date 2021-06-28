import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import r2_score

def import_data(folderpath, data_name):
    dfs = []
    for file in os.listdir(folderpath):
        if data_name in file:
            temp = pd.read_csv(folderpath + file)
            dfs.append(temp)

    total_df = pd.concat([df for df in dfs], axis=0)
    return total_df

#  Data Transformation:
#  1. Construct encoding object
#  2. Split data
#  3. Apply transformations
def data_preprocessing(raw_dataframe, categorical_cols, scale_cols, test_size = 0.1, random_state = 45):
    columntransformer = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), categorical_cols)], remainder='passthrough')

    raw_dataframe = raw_dataframe.drop(['Unnamed: 0'], axis=1)
    X_full = raw_dataframe.loc[:, raw_dataframe.columns!='length']
    y_full = raw_dataframe.length
    X_train, X_test, y_train, y_test = train_test_split(X_full, y_full, test_size=test_size, random_state=random_state, shuffle=True)

    X_train = columntransformer.fit_transform(X_train)
    X_test = columntransformer.transform(X_test)


    return [X_train, X_test, y_train, y_test]

def build_model(params):  #  Dictionary
    rf = RandomForestRegressor(**params)

    return rf

#  MAIN CODE

folderpath = "..\\data\\"
full_data = import_data(folderpath, "spring_age")
X_train, X_test, y_train, y_test = data_preprocessing(full_data, ['stock'], ['year'])

#  Random Forest Hyperparameters:
# trees= 100
# max_samples = 1000         #Number of training data points used for each bootstrapped sample
# min_samples_split = 2      #Min number of data points to split each tree at each node
# oob_score = True
# min_impurity_decrease = 0.1
# max_features
# min_samples_leaf
random_forest = build_model(
    {
        "n_estimators":100,
        "oob_score":True,
        "min_impurity_decrease":0.1
    }
)

sum_rsquared = 0
epochs = 10
for epoch in range(epochs):
    random_forest.fit(X_train, y_train)
    rf_score = random_forest.score(X_train, y_train)
    print(f"Epoch {epoch}; R squared: {rf_score}")
    sum_rsquared+=rf_score

average_rsquared = sum_rsquared/epochs

#  Grid Search
param_grid = {
    "n_estimators": [50,75,100,125,150,175,200],
    "max_features": [0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]

}
gridsearch = GridSearchCV(random_forest, param_grid=param_grid, n_jobs=-1)
gridsearch.fit(X_train, y_train)
final_model = gridsearch.best_estimator_









