import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

INCREMENTS_PATH = "C:/SuryaMain/Python Projects/ChinookUL/ChinookSalmonResearchProject/data"

def import_data(data_name = "spring_age", folderpath = INCREMENTS_PATH):
    spring_age_paths = []
    for file in os.listdir(folderpath):
        if data_name in file:
            spring_age_paths.append(os.path.join(folderpath, file))

    spring_age_data = pd.concat([pd.read_csv(file_path) for file_path in spring_age_paths], axis=0)

    return spring_age_data

def data_preprocessing(spring_age_data, categ_cols = "stock", test_size = 0.1, random_state = 45):
    X_full = spring_age_data.loc[:, spring_age_data.columns != 'length']
    y_full = spring_age_data.length

    if categ_cols is not None:
        X_stock = X_full[categ_cols]
        X_full = X_full.drop(categ_cols, axis=1)
        X_full = pd.concat([X_full, X_stock], axis=1)

        X_full = pd.get_dummies(X_full, columns=[categ_cols])
        X_full = X_full.drop('Unnamed: 0', axis=1)

    X_train, X_test, y_train, y_test = train_test_split(X_full, y_full, test_size=0.1, random_state=45, shuffle=True)

    X_train.reset_index(drop=True, inplace=True)
    X_test.reset_index(drop=True, inplace=True)
    y_train.reset_index(drop=True, inplace=True)
    y_test.reset_index(drop=True, inplace=True)

    scaler = StandardScaler()
    scaled_df_train = pd.DataFrame(scaler.fit_transform(X_train[[scale_cols]]))
    scaled_df_train.rename(columns={0: 'year'}, inplace=True)

    X_train = X_train.loc[:, X_train.columns != 'year'].join(scaled_df_train)

    scaled_df_test = pd.DataFrame(scaler.fit_transform(X_test[['year']]))
    scaled_df_test.rename(columns={0: 'year'}, inplace=True)
    X_test = X_test.loc[:, X_test.columns != 'year'].join(scaled_df_test)


    return [X_train, X_test, y_train, y_test]

