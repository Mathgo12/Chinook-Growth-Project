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

SIMULATION_BASEPATH = "C:/SuryaMain/Python Projects/ChinookUL/ChinookSalmonResearchProject/simulate_nonlinear_data"

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
    r2_train = rf_model.get_rsquared()
    test_pred, r2_test = rf_model.predict(X_test, y_test)

    return [rf_model, (r2_train, r2_test)]


def main():
    r2_train_vals = []
    r2_test_vals = []
    total_effects = []
    for data_path in os.listdir(SIMULATION_BASEPATH):
        rf_model, (r2_train, r2_test) = train_sim_model(data_path)
        hyperparams = pd.read_csv(os.path.join(data_path, 'hyper_params.csv'))
        total_effect = hyperparams['total_effect'][0]
        nonlinear = hyperparams['nonlinear'][1]
        interactions = hyperparams


    df = pd.DataFrame({
        'r2 train': r2_train_vals,
        'r2 test': r2_test_vals,
        'totals_effects': total_effects
    })




if __name__ == "__main__":
    main()