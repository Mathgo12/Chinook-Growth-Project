#!/usr/bin/env python
# coding: utf-8

# In[82]:


import pandas as pd
import numpy as np
import matplotlib as plt
import numpy as np

# #**Data: dat_means_stock_wide.csv**

# In[83]:


data = pd.read_csv("data/dat_means_stock_wide.csv") #  Surya's Path
data = data.drop(columns=['Unnamed: 0'], axis=1)
data.head(10)


# In[ ]:


data_grouped = data.groupby(['release_type', 'run', 'sex', 'release_location_rmis_basin'])    #group all the stocks together


all_data_frames = []   #Stores all the grouped pandas data frames
years = []             #Stores all the years for each stock
average_length_age_3 = []     #Stores averages of the length_age3 values in each data frame
average_length_age_4 = []
average_length_age_5 = []

for name,df in data_grouped:
    all_data_frames.append(df)

for df in all_data_frames:
    years.append(int(df['brood_year'].median()))      #Add the median year to a list
    average_length_age_3.append(df['length_age3'].mean())   #Add the mean length at age 3 to a list
    average_length_age_4.append(df['length_age4'].mean()) 
    average_length_age_5.append(df['length_age5'].mean())


# In[ ]:



date_grouped = data.groupby(['release_type', 'run',  'release_location_rmis_basin']) 
df = date_grouped.app()


# In[ ]:


cluster_data = pd.DataFrame({'year': years,                        #New Data Frame with the lengths appended together
                             'length_age3': average_length_age_3,      
                             'length_age4': average_length_age_4, 
                             'length_age5': average_length_age_5
})
from sklearn.impute import SimpleImputer                           #For each column, make the NA values the mean of the row values
imputer = SimpleImputer(missing_values = np.nan, strategy='mean')
cluster_data_imputed = imputer.fit_transform(cluster_data).astype(object)
cluster_data_imputed = pd.DataFrame(data=cluster_data_imputed)


# # Kmeans

# In[ ]:


from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score  #Used to find the best number of clusters
inertias = {}
n_clusters = [i for i in range(2,16)]
ss = []
for i in n_clusters:
  km = KMeans(n_clusters = i)
  km.fit(cluster_data_imputed[['length_age3', 'length_age4', 'length_age5']])
  inertias[i] = km.inertia_
  ss.append(silhouette_score(cluster_data_imputed[['length_age3', 'length_age4', 'length_age5']], km.labels_))


# In[ ]:


import matplotlib.pyplot as plt     #Plot Cluster inertia (sum of squared errors) and K clusters
inertia_vals = list(inertias.values())
plt.plot(n_clusters, inertia_vals, c='blue')
plt.xlabel('Number of Clusters (n_clusters)')
plt.ylabel('Sum of Squared Errors (Inertia)')
plt.title('Number of Clusters K vs Model Inertia')
plt.xticks(np.arange(1,16))
plt.yticks(np.arange(0,300000,20000))
plt.grid()
plt.show()


# In[ ]:


plt.plot(n_clusters, ss, color='r')    #Plot Silhouette Scores and K Clusters
plt.xticks(np.arange(1,16))
plt.yticks(np.arange(0.4,0.6,0.02))
plt.grid()
plt.title('Number of Clusters K vs Silhouette Score')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()


# The optimal number of clusters seems to be 4 clusters, since the silhouette score is largest at 4 clusters

# In[ ]:


final_model = KMeans(n_clusters=4)
final_model.fit(cluster_data_imputed[['length_age3','length_age4', 'length_age5']])
predictions = final_model.predict(cluster_data_imputed[['length_age3','length_age4', 'length_age5']])

cluster_data_imputed['Clusters'] = predictions
cluster_centers = final_model.cluster_centers_
cluster_centers


# In[ ]:


cluster_data_imputed.to_csv('data/kmeans_dat_stock_wide.csv') ## Dataset used for K-means is exported


# In[ ]:


plt.plot(np.transpose(cluster_centers))


# # K-Means: females

# In[91]:


females = data.groupby(['sex']).get_group('F')
females_g = females.groupby(['release_type', 'run', 'release_location_rmis_basin'])
cluster_data_females = females_g.mean()


# In[92]:


d_cluster = []
for name, df in cluster_data_females.groupby('run'):
  df.fillna(df.mean(), inplace=True)
  #print(df[['length_age3']])
  d_cluster.append(df)
c_data_females = pd.concat(d_cluster, axis=0)
#c_data_females


# In[93]:


from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score  #Used to find the best number of clusters
inertias = {}
n_clusters = [i for i in range(2,16)]
ss = []
for i in n_clusters:
  km = KMeans(n_clusters = i)
  km.fit(c_data_females[['length_age4', 'length_age5']])
  inertias[i] = km.inertia_
  ss.append(silhouette_score(c_data_females[['length_age4', 'length_age5']], km.labels_))


# In[94]:


import matplotlib.pyplot as plt     #Plot Cluster inertia (sum of squared errors) and K clusters
inertia_vals = list(inertias.values())
plt.plot(n_clusters, inertia_vals, c='blue')
plt.xlabel('Number of Clusters (n_clusters)')
plt.ylabel('Sum of Squared Errors (Inertia)')
plt.title('Number of Clusters K vs Model Inertia')
plt.xticks(np.arange(1,16))
plt.grid()
plt.show()


# In[95]:


plt.plot(n_clusters, ss, color='r')    #Plot Silhouette Scores and K Clusters
plt.xticks(np.arange(1,16))
plt.grid()
plt.title('Number of Clusters K vs Silhouette Score')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()


# 5 clusters
# 

# In[160]:


kmeans = KMeans(n_clusters=5)
kmeans.fit(c_data_females[['length_age4', 'length_age5']])
predictions = kmeans.predict(c_data_females[['length_age4', 'length_age5']])
c_data_females['clusters_5'] = predictions
plt.scatter(c_data_females['length_age4'], c_data_females['length_age5'], c = c_data_females['clusters_5'], cmap='viridis')
plt.grid()
plt.title('Females: length at age 4 vs 5')
plt.show()


# 3 Clusters

# In[161]:


kmeans = KMeans(n_clusters=3)
kmeans.fit(c_data_females[['length_age4', 'length_age5']])
predictions = kmeans.predict(c_data_females[['length_age4', 'length_age5']])
c_data_females['clusters_3'] = predictions
plt.scatter(c_data_females['length_age4'], c_data_females['length_age5'], c = c_data_females['clusters_3'], cmap='viridis')
plt.grid()
plt.title('Females: length at age 4 vs 5')
plt.show()


# 2 clusters
# 

# In[162]:


#K-means with 2 clusters
kmeans = KMeans(n_clusters=2)
kmeans.fit(c_data_females[['length_age4', 'length_age5']])
predictions = kmeans.predict(c_data_females[['length_age4', 'length_age5']])
c_data_females['clusters_2'] = predictions
plt.scatter(c_data_females['length_age4'], c_data_females['length_age5'], c = c_data_females['clusters_2'], cmap='viridis')
plt.grid()
plt.title('Females: length at age 4 vs 5')
plt.show()


# In[ ]:


c_data_females.reset_index()


# Categorical Data for each cluster

# In[147]:


# 2 Clusters 
f_release_types_1_2c = c_data_females[c_data_females['clusters_2'] == 0].release_type.value_counts()  # All but 1 are one_YO_summer,  1 meaning cluster 1, 2c meaning 2 clusters used
f_release_types_2_2c = c_data_females[c_data_females['clusters_2'] == 1].release_type.value_counts()  # All but 1 are two_YO_releases

f_runs_1_2c = c_data_females[c_data_females['clusters_2'] == 0].run.value_counts()    #Most have a run type of 3
f_runs_2_2c = c_data_females[c_data_females['clusters_2'] == 1].run.value_counts()    #Most have a run type of 1

f_release_locations1_2c = c_data_females[c_data_females['clusters_2'] == 0].release_location_rmis_basin.value_counts()   #varied
f_release_locations2_2c = c_data_females[c_data_females['clusters_2'] == 1].release_location_rmis_basin.value_counts()   #Varied

#3 Clusters
f_release_types_1_3c = c_data_females[c_data_females['clusters_3'] == 0].release_type.value_counts()  # All are one_YO_summer
f_release_types_2_3c = c_data_females[c_data_females['clusters_3'] == 1].release_type.value_counts()  # 6/8 are two_YO_releases
f_release_types_3_3c = c_data_females[c_data_females['clusters_3'] == 2].release_type.value_counts()  # all are two_YO_releases

f_runs_1_3c = c_data_females[c_data_females['clusters_3'] == 0].run.value_counts()    #Most have a run type of 3
f_runs_2_3c = c_data_females[c_data_females['clusters_3'] == 1].run.value_counts()    #Varied, 3 have run type 3
f_runs_3_3c = c_data_females[c_data_females['clusters_3'] == 2].run.value_counts()    #Most have a run type of 1, (7)

f_release_locations1_3c = c_data_females[c_data_females['clusters_3'] == 0].release_location_rmis_basin.value_counts()     #all are varied  
f_release_locations2_3c = c_data_females[c_data_females['clusters_3'] == 1].release_location_rmis_basin.value_counts()  
f_release_locations3_3c = c_data_females[c_data_females['clusters_3'] == 2].release_location_rmis_basin.value_counts()   


# In[167]:


# K-means with 2 clusters
f_cluster1_stats = pd.concat([f_release_types_1_2c, f_runs_1_2c, f_release_locations1_2c], axis=0)
f_cluster2_stats = pd.concat([f_release_types_2_2c, f_runs_2_2c, f_release_locations2_2c], axis=0)
f_cluster2_stats


# # K-Means: males

# In[142]:


males = data.groupby(['sex']).get_group('M')
males_g = males.groupby(['release_type', 'run', 'release_location_rmis_basin'])
cluster_data_males = males_g.mean()

males_df_list = []
for name, df in cluster_data_males.groupby('run'):
  df.fillna(df.mean(), inplace=True)
  #print(df[['length_age3']])
  males_df_list.append(df)
c_data_males = pd.concat(males_df_list, axis=0)


from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score  #Used to find the best number of clusters
inertias2 = {}
n_clusters = [i for i in range(2,16)]
ss = []
for i in n_clusters:
  km = KMeans(n_clusters = i)
  km.fit(c_data_males[['length_age3', 'length_age4', 'length_age5']])
  inertias2[i] = km.inertia_
  ss.append(silhouette_score(c_data_males[['length_age3','length_age4', 'length_age5']], km.labels_))



# In[143]:


import matplotlib.pyplot as plt     #Plot Cluster inertia (sum of squared errors) and K clusters
inertia_vals2 = list(inertias2.values())
plt.plot(n_clusters, inertia_vals2, c='blue')
plt.xlabel('Number of Clusters (n_clusters)')
plt.ylabel('Sum of Squared Errors (Inertia)')
plt.title('Number of Clusters K vs Model Inertia')
plt.xticks(np.arange(1,16))
plt.grid()
plt.show()


# In[144]:


plt.plot(n_clusters, ss, color='r')    #Plot Silhouette Scores and K Clusters
plt.xticks(np.arange(1,16))
plt.grid()
plt.title('Number of Clusters K vs Silhouette Score')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()


# 2 clusters
# 

# In[145]:


kmeans_males = KMeans(n_clusters=2)
kmeans_males.fit(c_data_males)
predictions_males = kmeans_males.predict(c_data_males)
c_data_males['clusters_2'] = predictions_males

from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
components = pca.fit_transform(c_data_males[['length_age3', 'length_age4', 'length_age5']])
c_data_males_pca = pd.DataFrame(data=components)

fig, axes = plt.subplots(2,2)
fig.set_figheight(10)
fig.set_figwidth(10)
#PCA plot
axes[0,0].scatter(c_data_males_pca.iloc[:, 0], c_data_males.iloc[:, 1], c = predictions_males, cmap='viridis')
axes[0,0].grid()
axes[0,0].set_title('PCA plot')

# Length at age 3 vs 4
axes[0,1].scatter(c_data_males['length_age3'], c_data_males['length_age4'], c = predictions_males, cmap='viridis')
axes[0,1].grid()
axes[0,1].set_title('Length at age 3 vs 4')

#Length at age 3 vs 5
axes[1,0].scatter(c_data_males['length_age3'], c_data_males['length_age5'], c = predictions_males, cmap='viridis')
axes[1,0].grid()
axes[1,0].set_title('Length at age 3 vs 5')

#Length at age 4 vs 5
axes[1,1].scatter(c_data_males['length_age4'], c_data_males['length_age5'], c = predictions_males, cmap='viridis')
axes[1,1].grid()
axes[1,1].set_title('Length at age 4 vs 5')

plt.show()


# 3 clusters
# 

# In[146]:


kmeans_males = KMeans(n_clusters=3)
kmeans_males.fit(c_data_males)
predictions_males = kmeans_males.predict(c_data_males)
c_data_males['clusters_3'] = predictions_males

from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
components = pca.fit_transform(c_data_males[['length_age3', 'length_age4', 'length_age5']])
c_data_males_pca = pd.DataFrame(data=components)

fig, axes = plt.subplots(2,2)
fig.set_figheight(10)
fig.set_figwidth(10)
#PCA plot
axes[0,0].scatter(c_data_males_pca.iloc[:, 0], c_data_males.iloc[:, 1], c = predictions_males, cmap='viridis')
axes[0,0].grid()
axes[0,0].set_title('PCA plot')

# Length at age 3 vs 4
axes[0,1].scatter(c_data_males['length_age3'], c_data_males['length_age4'], c = predictions_males, cmap='viridis')
axes[0,1].grid()
axes[0,1].set_title('Length at age 3 vs 4')

#Length at age 3 vs 5
axes[1,0].scatter(c_data_males['length_age3'], c_data_males['length_age5'], c = predictions_males, cmap='viridis')
axes[1,0].grid()
axes[1,0].set_title('Length at age 3 vs 5')

#Length at age 4 vs 5
axes[1,1].scatter(c_data_males['length_age4'], c_data_males['length_age5'], c = predictions_males, cmap='viridis')
axes[1,1].grid()
axes[1,1].set_title('Length at age 4 vs 5')

plt.show()


# In[150]:


c_data_males.reset_index(inplace=True)


# In[151]:


# 2 Clusters 
m_release_types_1_2c = c_data_males[c_data_males['clusters_2'] == 0].release_type.value_counts()  
m_release_types_2_2c = c_data_males[c_data_males['clusters_2'] == 1].release_type.value_counts() 

m_runs_1_2c = c_data_males[c_data_males['clusters_2'] == 0].run.value_counts()    
m_runs_2_2c = c_data_males[c_data_males['clusters_2'] == 1].run.value_counts()   

m_release_locations1_2c = c_data_males[c_data_males['clusters_2'] == 0].release_location_rmis_basin.value_counts()   #varied
m_release_locations2_2c = c_data_males[c_data_males['clusters_2'] == 1].release_location_rmis_basin.value_counts()   #Varied

#3 Clusters
m_release_types_1_3c = c_data_males[c_data_males['clusters_3'] == 0].release_type.value_counts()  
m_release_types_2_3c = c_data_males[c_data_males['clusters_3'] == 1].release_type.value_counts()  
m_release_types_3_3c = c_data_males[c_data_males['clusters_3'] == 2].release_type.value_counts() 

m_runs_1_3c = c_data_males[c_data_males['clusters_3'] == 0].run.value_counts()    
m_runs_2_3c = c_data_males[c_data_males['clusters_3'] == 1].run.value_counts()    
m_runs_3_3c = c_data_males[c_data_males['clusters_3'] == 2].run.value_counts()    

m_release_locations1_3c = c_data_males[c_data_males['clusters_3'] == 0].release_location_rmis_basin.value_counts()     #all are varied  
m_release_locations2_3c = c_data_males[c_data_males['clusters_3'] == 1].release_location_rmis_basin.value_counts()  
m_release_locations3_3c = c_data_males[c_data_males['clusters_3'] == 2].release_location_rmis_basin.value_counts()   


# In[152]:


#2 clusters
m_cluster1_stats = pd.concat([m_release_types_1_2c, m_runs_1_2c, m_release_locations1_2c], axis=0)
m_cluster2_stats = pd.concat([m_release_types_2_2c, m_runs_2_2c, m_release_locations2_2c], axis=0)
print(m_cluster1_stats)
print(m_cluster2_stats)


# # K-Means: all data

# In[53]:


all_data_g = data.groupby(['release_type', 'run', 'sex','release_location_rmis_basin'])
all_data = all_data_g.mean()

df_list = []
for name, df in all_data.groupby('run'):
  df.fillna(df.mean(), inplace=True)
  #print(df[['length_age3']])
  df_list.append(df)
c_data = pd.concat(df_list, axis=0)


from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score  #Used to find the best number of clusters
inertias = {}
n_clusters = [i for i in range(2,16)]
ss = []
for i in n_clusters:
  km = KMeans(n_clusters = i)
  km.fit(c_data[['length_age3', 'length_age4', 'length_age5']])
  inertias[i] = km.inertia_
  ss.append(silhouette_score(c_data[['length_age3','length_age4', 'length_age5']], km.labels_))


# In[54]:


import matplotlib.pyplot as plt     #Plot Cluster inertia (sum of squared errors) and K clusters
inertia_vals = list(inertias.values())
plt.plot(n_clusters, inertia_vals, c='blue')
plt.xlabel('Number of Clusters (n_clusters)')
plt.ylabel('Sum of Squared Errors (Inertia)')
plt.title('Number of Clusters K vs Model Inertia')
plt.xticks(np.arange(1,16))
plt.grid()
plt.show()


# In[55]:


plt.plot(n_clusters, ss, color='r')    #Plot Silhouette Scores and K Clusters
plt.xticks(np.arange(1,16))
plt.grid()
plt.title('Number of Clusters K vs Silhouette Score')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Score')
plt.show()


# 2 clusters
# 

# In[153]:


kmeans = KMeans(n_clusters=2)
kmeans.fit(c_data)
predictions = kmeans.predict(c_data)
c_data['clusters_2'] = predictions


from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
components = pca.fit_transform(c_data[['length_age3', 'length_age4', 'length_age5']])
c_data_pca = pd.DataFrame(data=components)

fig, axes = plt.subplots(2,2)
fig.set_figheight(10)
fig.set_figwidth(10)
#PCA plot
axes[0,0].scatter(c_data_pca.iloc[:, 0], c_data.iloc[:, 1], c = predictions, cmap='viridis')
axes[0,0].grid()
axes[0,0].set_title('PCA plot')

# Length at age 3 vs 4
axes[0,1].scatter(c_data['length_age3'], c_data['length_age4'], c = predictions, cmap='viridis')
axes[0,1].grid()
axes[0,1].set_title('Length at age 3 vs 4')

#Length at age 3 vs 5
axes[1,0].scatter(c_data['length_age3'], c_data['length_age5'], c = predictions, cmap='viridis')
axes[1,0].grid()
axes[1,0].set_title('Length at age 3 vs 5')

#Length at age 4 vs 5
axes[1,1].scatter(c_data['length_age4'], c_data['length_age5'], c = predictions, cmap='viridis')
axes[1,1].grid()
axes[1,1].set_title('Length at age 4 vs 5')

plt.show()


# 3 clusters
# 

# In[154]:


kmeans = KMeans(n_clusters=3)
kmeans.fit(c_data)
predictions = kmeans.predict(c_data)
c_data['clusters_3'] = predictions


from sklearn.decomposition import PCA
pca = PCA(n_components = 2)
components = pca.fit_transform(c_data[['length_age3', 'length_age4', 'length_age5']])
c_data_pca = pd.DataFrame(data=components)

fig, axes = plt.subplots(2,2)
fig.set_figheight(10)
fig.set_figwidth(10)
#PCA plot
axes[0,0].scatter(c_data_pca.iloc[:, 0], c_data.iloc[:, 1], c = predictions, cmap='viridis')
axes[0,0].grid()
axes[0,0].set_title('PCA plot')

# Length at age 3 vs 4
axes[0,1].scatter(c_data['length_age3'], c_data['length_age4'], c = predictions, cmap='viridis')
axes[0,1].grid()
axes[0,1].set_title('Length at age 3 vs 4')

#Length at age 3 vs 5
axes[1,0].scatter(c_data['length_age3'], c_data['length_age5'], c = predictions, cmap='viridis')
axes[1,0].grid()
axes[1,0].set_title('Length at age 3 vs 5')

#Length at age 4 vs 5
axes[1,1].scatter(c_data['length_age4'], c_data['length_age5'], c = predictions, cmap='viridis')
axes[1,1].grid()
axes[1,1].set_title('Length at age 4 vs 5')

plt.show()


# In[157]:


c_data.reset_index(inplace=True)


# In[158]:


# 2 Clusters 
release_types_1_2c = c_data[c_data['clusters_2'] == 0].release_type.value_counts()  
release_types_2_2c = c_data[c_data['clusters_2'] == 1].release_type.value_counts()  

runs_1_2c = c_data[c_data['clusters_2'] == 0].run.value_counts()    
runs_2_2c = c_data[c_data['clusters_2'] == 1].run.value_counts()    

release_locations1_2c = c_data[c_data['clusters_2'] == 0].release_location_rmis_basin.value_counts()   #varied
release_locations2_2c = c_data[c_data['clusters_2'] == 1].release_location_rmis_basin.value_counts()   #Varied

#3 Clusters
release_types_1_3c = c_data[c_data['clusters_3'] == 0].release_type.value_counts()  
release_types_2_3c = c_data[c_data['clusters_3'] == 1].release_type.value_counts()  
release_types_3_3c = c_data[c_data['clusters_3'] == 2].release_type.value_counts()  

runs_1_3c = c_data[c_data['clusters_3'] == 0].run.value_counts()    
runs_2_3c = c_data[c_data['clusters_3'] == 1].run.value_counts()    
runs_3_3c = c_data[c_data['clusters_3'] == 2].run.value_counts()   

release_locations1_3c = c_data[c_data['clusters_3'] == 0].release_location_rmis_basin.value_counts()   
release_locations2_3c = c_data[c_data['clusters_3'] == 1].release_location_rmis_basin.value_counts()  
release_locations3_3c = c_data[c_data['clusters_3'] == 2].release_location_rmis_basin.value_counts()   


# In[159]:


cluster1_stats = pd.concat([release_types_1_2c, runs_1_2c, release_locations1_2c], axis=0)
cluster2_stats = pd.concat([release_types_2_2c, runs_2_2c, release_locations2_2c], axis=0)
print(cluster1_stats)
print(cluster2_stats)

