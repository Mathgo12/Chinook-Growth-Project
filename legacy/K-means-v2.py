#!/usr/bin/env python
# coding: utf-8

# # Data: dat_means_stock.csv

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
import numpy as np


# In[ ]:


data = pd.read_csv("data/dat_means_stock.csv")
data = data.drop(columns=['Unnamed: 0', 'release_length'], axis=1)
data.head(10)


# In[ ]:


data_grouped = data_grouped = data.groupby(['release_type', 'run', 'sex', 'release_location_rmis_basin'])
all_data_frames = [] 
ages = []
brood_years = []
lengths = []
y_ns = []

for name,df in data_grouped:
    all_data_frames.append(df)

for df in all_data_frames:
    #ages.append(df['age'].mean())
    lengths.append(df['length'].mean())
    y_ns.append(int(df['y_n'].median()))

cluster_data = pd.DataFrame({#'age':ages,
                             'length': lengths,      
                             'y_n': y_ns })
cluster_data


# In[ ]:


from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
cluster_data_scaled = pd.DataFrame(scaler.fit_transform(cluster_data))
cluster_data = cluster_data_scaled.rename(columns={0:'length', 1: 'y_n'})
cluster_data


# In[ ]:


#K-means is run on the length and y_n columns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score  #Used to find the best number of clusters
inertias = {}
n_clusters = [i for i in range(2,16)]         #K-Means is trained with multiple numbers of clusters (in order to find the best number)
ss = []
for i in n_clusters:
  km = KMeans(n_clusters = i)
  km.fit(cluster_data)
  inertias[i] = km.inertia_
  ss.append(silhouette_score(cluster_data, km.labels_))


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
plt.grid()
plt.title('Number of Clusters K vs Silhouette Score')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()


# In[ ]:


km2 = KMeans(n_clusters=3)
km2.fit(cluster_data)
predictions = km2.predict(cluster_data)
centroids = km2.cluster_centers_
plt.grid()
plt.scatter(cluster_data['length'], cluster_data['y_n'], c=predictions, cmap='plasma')
plt.scatter(centroids[:, 0], centroids[:,1])
plt.show()

##  Scatter plot with scaled values


# In[ ]:


centroids_df = pd.DataFrame(centroids, columns = ['length', 'y_n'])
cluster_data2 = cluster_data.append(centroids_df, ignore_index=True)
cluster_data2


# In[ ]:


cluster_data2_unscaled = pd.DataFrame(scaler.inverse_transform(cluster_data2)).rename(columns = {0:'length', 1:'y_n'})
# y_n data type converted to integer
cluster_data2_unscaled.iloc[:,1] = cluster_data2_unscaled.iloc[:, 1].astype(int)  
#Plot with centroids
plt.scatter(cluster_data2_unscaled.iloc[0:-3, 0], cluster_data2_unscaled.iloc[0:-3, 1], c = predictions, cmap='plasma')
plt.scatter(cluster_data2_unscaled.iloc[-3:, 0], cluster_data2_unscaled.iloc[-3:, 1], c = 'blue', s = 80)
plt.grid()
plt.xlabel('Length')
plt.ylabel('y_n')
plt.show()

## Scatter plot with original length and y_n values


# In[ ]:


cluster_data2_unscaled #Original data for clustering with the 3 cluster centroids added (indices 60-62)

