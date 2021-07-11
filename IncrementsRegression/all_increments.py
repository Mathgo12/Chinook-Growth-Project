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

def data_preprocessing(raw_dataframe, categorical_cols, scale_cols, test_size = 0.1, random_state = 45):
    columntransformer = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), categorical_cols)], remainder='passthrough')

    raw_dataframe = raw_dataframe.drop(['Unnamed: 0'], axis=1)
    X_full = raw_dataframe.loc[:, raw_dataframe.columns!='length']
    y_full = raw_dataframe.length
    X_train, X_test, y_train, y_test = train_test_split(X_full, y_full, test_size=test_size, random_state=random_state, shuffle=True)

    X_train = columntransformer.fit_transform(X_train)
    X_test = columntransformer.transform(X_test)


    return [X_train, X_test, y_train, y_test]

def train_model(params, X_train, y_train, epochs=15):
    """
    :param params:
    :param X_train:
    :param y_train:
    :param epochs:
    :return: [rf, average_rquared]

    # Random Forest Hyperparameters:
    # n_estimators
    # max_samples          #Number of training data points used for each bootstrapped sample
    # min_samples_split     #Min number of data points to split each tree at each node
    # oob_score
    # min_impurity_decrease
    # max_features
    # min_samples_leaf

    """
    rf = RandomForestRegressor(**params)

    sum_rsquared = 0
    epochs = epochs
    for epoch in range(epochs):
        rf.fit(X_train, y_train)
        rf_score = rf.score(X_train, y_train)
        #print(f"Epoch {epoch}; R squared: {rf_score}")
        sum_rsquared += rf_score

    average_rsquared = sum_rsquared / epochs
    return [rf, average_rsquared]

