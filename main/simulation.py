import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.base import RegressorMixin, BaseEstimator
from sklearn.inspection import partial_dependence
from ChinookSalmonResearchProject.IncrementsRegression import model
#from ChinookSalmonResearchProject.IncrementsRegression.increments_processing import import_data, data_preprocessing

BASEPATH = 'C:/SuryaMain/Python Projects/ChinookUL/ChinookSalmonResearchProject'
SIMULATION_BASEPATH = os.path.join(BASEPATH, "simulate_nonlinear_data")

def train_sim_model(data_path = os.path.join(SIMULATION_BASEPATH, 'data_set_1')):
    X = pd.read_csv(os.path.join(data_path, 'X.csv'))
    y = pd.read_csv(os.path.join(data_path, 'y.csv'))

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.1, random_state=12)

    params = {
        "n_estimators": 100,
        "oob_score": True,
        "min_impurity_decrease": 0.1
    }
    rf_model = model.RFRegressor(params = params)
    rf_model.fit(X_train,y_train)
    r2_train = rf_model.rsquared
    test_pred, r2_test = rf_model.predict(X_test, y_test)

    return [rf_model, (r2_train, r2_test)]

def sim_dataframe(simulation_datapath = SIMULATION_BASEPATH):
    features = []
    r2_train_vals = []
    r2_test_vals = []
    total_effects = []
    nonlinear_vals = []
    interactions_vals = []
    rhoX_vals = []
    intX_vals = []
    rhoU_vals = []
    intU_vals = []

    for data_path in os.listdir(simulation_datapath):
        if "data_set_" in data_path:
            full_datapath = os.path.join(SIMULATION_BASEPATH,data_path)
            rf_model, (r2_train, r2_test) = train_sim_model(data_path = full_datapath)
            hyperparams = pd.read_csv(os.path.join(full_datapath, 'hyper_params.csv'))

            features.append(hyperparams['m'][0])
            r2_train_vals.append(r2_train)
            r2_test_vals.append(r2_test)
            total_effects.append(hyperparams['total_effect'][0])
            nonlinear_vals.append(hyperparams['nonlinear'][0])
            interactions_vals.append(hyperparams['interactions'][0])
            rhoX_vals.append(hyperparams['rho_X'][0])
            intX_vals.append(hyperparams['int_X'][0])
            rhoU_vals.append(hyperparams['rho_U'][0])
            intU_vals.append(hyperparams['int_U'][0])

    df = pd.DataFrame({
        'features': features,
        'r2_train': r2_train_vals,
        'r2_test': r2_test_vals,
        'totals_effect': total_effects,
        'nonlinear': nonlinear_vals,
        'interactions': interactions_vals,
        'rho_X': rhoX_vals,
        'int_X': intX_vals,
        'rho_U': rhoU_vals,
        'int_U': intU_vals

    })

    return df

def main():
    simulation_results = sim_dataframe()
    simulation_results.to_csv(os.path.join(BASEPATH, 'main', 'sim_results2.csv'), index=False)

    #rf_model, (r2_train, r2_test), X_train = train_sim_model()
    # features = [0,1]
    # model.RFRegressor.pd_plot(rf_model, X_train, features)



if __name__ == "__main__":
    main()