import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

path = "legacy_data/Regression Data/"

data_COWL_fall = pd.read_csv(path + "regression_data_COWL_fall.csv")  # Surya's Path to File
data_COWL_spring = pd.read_csv(path + "regression_data_COWL_spring.csv")  # Surya's Path to File
data_DESC_spring = pd.read_csv(path + "regression_data_DESC_spring.csv")  # Surya's Path to File
data_YOCL_fall = pd.read_csv(path + "regression_data_YOCL_fall.csv")  # Surya's Path to File

#  groups of similar stocks
data_fall_GOA = pd.read_csv(path + "regression_data_fall_GOA.csv")  # Surya's Path to File
data_fall_NCC = pd.read_csv(path + "regression_data_fall_NCC.csv")  # Surya's Path to File
data_spring_GOA = pd.read_csv(path + "regression_data_spring_GOA.csv")  # Surya's Path to File
data_spring_NCC = pd.read_csv(path + "regression_data_spring_NCC.csv")  # Surya's Path to File

#  All stocks, mean length is normalized
data_mean_zero = pd.read_csv(path + "regression_data_mean_zero.csv")  # Surya's Path to File

#  Data editing
data_COWL_fall = data_COWL_fall.drop(['Unnamed: 0', 'release_type', 'stock', 'p52.5','run'], axis=1)
data_COWL_spring = data_COWL_spring.drop(['Unnamed: 0', 'release_type','stock', 'p52.5', 'run'], axis=1)
data_DESC_spring = data_DESC_spring.drop(['Unnamed: 0', 'release_type', 'stock'], axis=1)
data_YOCL_fall = data_YOCL_fall.drop(['Unnamed: 0', 'release_type', 'stock'], axis=1)


# Growth Increments
# 

# In[29]:

'''
increments_GOA_fall_age_1_2 = pd.read_csv(path + 'increments_GOA_fall_age_1_2.csv')
increments_GOA_fall_age_1_2.drop(increments_GOA_fall_age_1_2.columns[0], axis=1, inplace=True)
climate_vars = increments_GOA_fall_age_1_2.columns[3:]
dummy_vars_incGF12 = pd.get_dummies(increments_GOA_fall_age_1_2.stock, drop_first=True)
increments_GOA_fall_age_1_2 = pd.concat([increments_GOA_fall_age_1_2, dummy_vars_incGF12], axis=1).drop('stock', axis=1)
X_incGF12 = increments_GOA_fall_age_1_2.loc[:, increments_GOA_fall_age_1_2.columns != 'length'].values
y_incGF12 = increments_GOA_fall_age_1_2.loc[:, increments_GOA_fall_age_1_2.columns == 'length'].values.ravel()
x_incGF12_train, x_incGF12_test, y_incGF12_train, y_incGF12_test = train_test_split(X_incGF12, y_incGF12, test_size=0.2,random_state=24)

#  Decision Tree
trees = 200
oob_score_ = True
rf = RandomForestRegressor(n_estimators=trees, oob_score=oob_score_, min_samples_leaf=5)
rf.fit(x_incGF12_train, y_incGF12_train)
print(x_incGF12_test.shape[0])
'''