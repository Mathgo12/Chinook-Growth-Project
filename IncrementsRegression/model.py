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
from sklearn.inspection import partial_dependence, plot_partial_dependence

class RFRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, params = None):
        self.hparams = params
        self.model = RandomForestRegressor(**self.hparams)
        self.rsquared = None #  Only using training data
        self.istrained = False

    def __str__(self):
        return self.hparams

    def fit(self, X_train, y_train):
        self.model.fit(X_train,y_train)
        self.rsquared = self.model.score(X_train,y_train)
        self.istrained = True

    def predict(self, X, y=None):
        pred = self.model.predict(X)
        if y is not None:
            pred_rsquared = r2_score(y, pred)
            return [pred, pred_rsquared]
        else:
            return pred

    @classmethod
    def pd_plot(cls,model, X, features):
        plot_partial_dependence(model, X=X, features=features, n_jobs=-1)

    def vi_plot(self):
        pass

    def ice_plot(self):
        pass



if __name__ == '__main__':
    params = {
                "n_estimators":100,
                "oob_score":True,
                "min_impurity_decrease":0.1
            }
    test_rf = RFRegressor(params = params)

    data = increments_processing.import_data(datafolder_path, "spring_age")
    X_train, X_test, y_train, y_test = increments_processing.data_preprocessing(data, ['stock'], ['year'])
    test_rf.fit(X_train, y_train)
    test_rf.pd_plot(X_train, 2)