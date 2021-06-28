#!/usr/bin/env python
# coding: utf-8

# # Dimension Reduction
# This notebook contains code to run several dimension reduction techniques to help visualize the stricture in the chinook growth data set
# 
# 

# # PCA: dat_means_stock_wide.csv

# In[2]:


import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
import numpy as np

# In[ ]:


data = pd.read_csv("data/kmeans_dat_stock_wide.csv")
data = data.drop('Unnamed: 0', axis=1)
data['year'] = data['year'].astype(int)
data


# In[ ]:


from sklearn.decomposition import PCA
pca = PCA(n_components=2)
data_pca = pd.DataFrame(data=pca.fit_transform(data[['length_age3', 'length_age4', 'length_age5']]))


# In[ ]:


data_pca = data_pca.rename(columns = {0:'Col 1', 1:'Col 2'})
data_pca


# In[ ]:


import matplotlib.pyplot as plt
plt.grid(linestyle='--')
plt.scatter(data_pca['Col 1'], data_pca['Col 2'], c = data['Clusters'], cmap = 'seismic')
plt.xlabel('PCA Col 1')
plt.ylabel('PCA Col 2')
plt.title('PCA Dimension-Reduced Length Values')       #The lengths at ages 3,4 and 5 were reduced to 2 features
plt.axis([-200, 200, -100, 100])
plt.xticks(np.arange(-200, 200, 50))
plt.yticks(np.arange(-100, 100, 20))
plt.show()


# # PCA: dat_weights.csv
# 

# In[ ]:


data = pd.read_csv("data/kmeans_dat_weights.csv")
data = data.drop(columns=['Unnamed: 0'], axis=1)
data


# In[11]:


from sklearn.decomposition import PCA
pca = PCA(n_components=2)
data_pca = pd.DataFrame(data=pca.fit_transform(data.iloc[:,:-1]))


# In[ ]:


data_pca = data_pca.rename(columns = {0:'Col 1', 1:'Col 2'})
data_pca


# In[19]:


import matplotlib.pyplot as plt
plt.grid(linestyle='--')
plt.scatter(data_pca['Col 1'], data_pca['Col 2'], c = data['Clusters'], cmap='viridis')
plt.xlabel('PCA Col 1')
plt.ylabel('PCA Col 2')
plt.title('PCA Dimension-Reduced Length Values') #The three weights were reduced to 2 features 

plt.show()

