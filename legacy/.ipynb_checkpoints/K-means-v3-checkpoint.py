#!/usr/bin/env python
# coding: utf-8

# # Data: dat_weights.csv

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib as plt
import numpy as np


# In[ ]:


data = pd.read_csv("data/dat_weights.csv")
data = data.drop(columns=['Unnamed: 0', 'stock'], axis=1)
data.head(10)


# In[ ]:



#K-means is run on the length and y_n columns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score  #Used to find the best number of clusters
inertias = {}
n_clusters = [i for i in range(2,16)]         #K-Means is trained with multiple numbers of clusters (in order to find the best number)
ss = []
for i in n_clusters:
  km = KMeans(n_clusters = i)
  km.fit(data)
  inertias[i] = km.inertia_
  ss.append(silhouette_score(data, km.labels_))


# In[ ]:


import matplotlib.pyplot as plt     #Plot Cluster inertia (sum of squared errors) and K clusters
inertia_vals = list(inertias.values())
plt.plot(n_clusters, inertia_vals, c='blue')
plt.xlabel('Number of Clusters (n_clusters)')
plt.ylabel('Sum of Squared Errors (Inertia)')
plt.title('Number of Clusters K vs Model Inertia')
plt.xticks(np.arange(1,16))
plt.grid()
plt.show()


# In[ ]:


plt.plot(n_clusters, ss, color='r')    #Plot Silhouette Scores and K Clusters
plt.xticks(np.arange(1,16))
plt.grid()
plt.title('Number of Clusters K vs Silhouette Score')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()


# In[ ]:


final_model = KMeans(n_clusters=5)  #5 Clusters used for K-means
final_model.fit(data)
predictions = final_model.predict(data)

data['Clusters'] = predictions
cluster_centers = final_model.cluster_centers_
cluster_centers


# In[ ]:


data.to_csv('data/kmeans_dat_weights.csv')

