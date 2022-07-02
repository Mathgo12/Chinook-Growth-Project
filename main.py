import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pygam import LinearGAM, s, f, te, l
from sklearn.metrics import mean_squared_error
import math

BASEPATH = 'C:\SuryaMain\Python Projects\Chinook-Growth-Project'
SIMULATION_BASEPATH = os.path.join(BASEPATH, "simulate_nonlinear_data")
datasets = [name for name in os.listdir(SIMULATION_BASEPATH) if name[0:4] == 'data']


def get_data(fname):
    path = os.path.join(SIMULATION_BASEPATH, fname)
    if os.path.exists(path):
        X = pd.read_csv(os.path.join(path, 'X.csv'))
        X.drop(X.columns[0], axis=1, inplace=True)
        y = pd.read_csv(os.path.join(path, 'y.csv'))
        y.drop(y.columns[0], axis=1, inplace=True)
        return [X, y]
    else:
        print("Dataset does not exist")
        return [0, 0]


class SimGAM:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.model = None

    def train_lgam(self, **kwargs):
        gam = LinearGAM(**kwargs).fit(self.X, self.y)
        lams = []
        if 'lam' in kwargs.keys():
            lams = kwargs.get('lam')
        else:
            lams = np.logspace(-5, 5, 20) * len(self.X.columns)
        gam.gridsearch(self.X, self.y, lam=lams)
        self.model = gam

    def partial_dependences(self):
        # pds = []
        # for var in range(X.shape[1]):  # Number of variables
        #    sample = np.random.normal(0.0,1.0, 100)
        #    pdep = self.model.
        pass

    def calc_aic(self):
        if self.model is not None:
            num_params = len(self.model.coef_) + 1
            aic = -2 * self.model.loglikelihood(self.X, self.y) + 2 * num_params
            return aic
        else:
            print("Model Has Not Been Trained")
            return 0.0


def fill_vals(num_vars, var_idx):
    sample = np.zeros(shape=(100, num_vars))
    rand_vals = np.random.normal(0, 1, 100)
    for row_idx, row in enumerate(sample):
        row[var_idx] = rand_vals[row_idx]
    return sample


def pdp_test(model, nrows, ncols):
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)
    titles = list(map(lambda x: f'V{x}', np.arange(1, len(X.columns) + 1)))
    num_vars = model.X.shape[1]
    for i, ax in enumerate(axs):
        ##XX = model.model.generate_X_grid(term=i)
        sample = fill_vals(num_vars, i)
        ax.plot(sample[:, i], model.model.partial_dependence(term=i, X=sample))
        ax.plot(sample[:, i], model.model.partial_dependence(term=i, X=sample, width=.95)[1], c='r', ls='--')
        ax.set_title(titles[i]);
        ax.grid(True)
        print(sample.shape)
    plt.suptitle('Partial Dependence', size=16)
    fig.tight_layout()
    plt.show()


def pdp(model, nrows, ncols):
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols)
    titles = list(map(lambda x: f'V{x}', np.arange(1, len(X.columns) + 1)))
    for i, ax in enumerate(axs):
        XX = model.model.generate_X_grid(term=i)
        # sample = np.random.normal(0,1,100)
        ax.plot(XX[:, i], model.model.partial_dependence(term=i, X=XX))
        ax.plot(XX[:, i], model.model.partial_dependence(term=i, X=XX, width=.95)[1], c='r', ls='--')
        ax.set_title(titles[i]);
        ax.grid(True)
        print(type(XX))
        print(XX.shape)
    plt.suptitle('Partial Dependence', size=16)
    fig.tight_layout()
    plt.show()

dataset_1 = get_data('data_set_1')
X = dataset_1[0]
y = dataset_1[1]
gam = SimGAM(X, y)
gam.train_lgam(n_splines=16)
pdp_test(gam, 2, 1)