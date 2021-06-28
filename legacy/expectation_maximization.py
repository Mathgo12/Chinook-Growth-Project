#!/usr/bin/env python
# coding: utf-8

# This notebook has code to work with the pyGAM library for fitting generalied additive models. These models fit non-linear function to data and are useful for prediction and for interpolating between data points. Our goal will be to use them to describe the trends in the Chinook salmon growth data set. 
# 
# I have included code to work with the pyGAM library here. This seems like a fairly decent piece of software for fitting GAMs, but it is worth noting that the mgcv package in R does have more features. 
# 
# I also include some code to show how expectation maximization can be used to use GAMs for unsupervised clustering. 

# In[ ]:



# install pyGAM
get_ipython().system('pip install pygam')


# In[ ]:


# libraries
import pygam 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
# In[ ]:


# Load data
data = pd.read_csv("data/dat_means_stock_wide.csv") #Surya's Path to file
data = data.drop(columns=['Unnamed: 0'], axis=1)
data.head(10)


# In[ ]:


# create combined variable to identify stocks
data = data.assign(stock = data.release_type+data.sex+[str(i) for i in data.run]+data.release_location_rmis_basin)
# filter missing values

# filter data 
#data_filtered = data.query('length_age4 == length_age4') # filters out NaNs (NaN != NaN)
data_filtered = data[data.length_age4.notnull()]# create combined variable to identify stocks
data = data.assign(stock = data.release_type+data.sex+[str(i) for i in data.run]+data.release_location_rmis_basin)
# filter missing values

# filter data 
#data_filtered = data.query('length_age4 == length_age4') # filters out NaNs (NaN != NaN)
data_filtered = data[data.length_age4.notnull()]


# Now that the data is loaded we can start fittig GAMs. Although GAMs can be used for multivariate analysis, the code below fits the average length of age four fish as a univarite function of time. 
# 

# In[ ]:



# create predictor and target data frames 
data_y = pd.DataFrame({
    'y':data_filtered.length_age4
})

data_x = pd.DataFrame({
    'year':data_filtered.brood_year-1970
})

# fit GAM to length data 
from pygam import LinearGAM, s, f, te
gam = LinearGAM(s(0)).fit(data_x, data_y)

# Plot the trend predicted by the modela and the confidence intervals
XX = gam.generate_X_grid(term=0, n=200)
plt.plot(XX, gam.predict(XX), 'r--')
plt.plot(XX, gam.prediction_intervals(XX, width=.95), color='b', ls='--')


# In addition to computing predictions and confidence intervals we may also want to calculate the residuals, mean squared error or other model fit summary.  Residuals can be calculated using the predict method as shown below 

# In[ ]:


# predicted values of X
pred = gam.predict(data_x) 

# get residuals
resids = gam.predict(data_x) - data_y.y

# get MSE
MSE = sum((gam.predict(data_x) - data_y.y)**2)/len(data_y.y)
print(MSE)


# In[ ]:


# we can also plot the residuals as a function of time 
# to see if there are any trends that the model does not capture
plt.scatter(data_x, resids)


# Because GAMs are nonlinear functions a balance nees to be found between over and under fitting the data. In essence if the function is too wiggly it will overfit the data where as if the funciton is too smooth then it will not propperly reflect the true amount of underlying variation. 
# 
# For our purposes a function that over fits the data will over state the amount of differences between populaitons resulting in too many clusters, while a function that is too smooth will have the opposite problem. 
# 
# One way to adjust the smoothness of the function is by adjusting the number of splines as shown below. 

# In[ ]:


# set up multiple subplots
fig, axs = plt.subplots(2,2)

# set number of splines 
splines = [5,10,20,40]
fig_ind_x = [0,0,1,1]
fig_ind_y = [0,1,0,1]

# loop over numbers of splines 
for i in range(0,4):
  # fit gam 
  gam = LinearGAM(s(0, n_splines = splines[i])).fit(data_x, data_y)

  # Plot the trend predicted by the models and the confidence intervals
  XX = gam.generate_X_grid(term=0, n=200)
  axs[fig_ind_x[i], fig_ind_y[i]].plot(XX, gam.predict(XX), 'r--')
  axs[fig_ind_x[i], fig_ind_y[i]].plot(XX, gam.prediction_intervals(XX, width=.95), color='b', ls='--')
  axs[fig_ind_x[i], fig_ind_y[i]].set_title("number of splines" + str(splines[i]))

# x and y labels
for ax in axs.flat:
    ax.set(xlabel='Year', ylabel='length at age 4')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()


# We will need to fit splines for differnt groups of stocks. The easiest way to do this with pyGAM is to create differnt data frames and fit seperate models to each of these data frames. In the block below I have fit a unique gam for each run type and plotted them.

# In[ ]:


# set up multiple subplots
fig, axs = plt.subplots(2,2)

# set number of splines 
runs = [1,2,3,8]
titles = ["spring","summer","fall","late fall"]
fig_ind_x = [0,0,1,1]
fig_ind_y = [0,1,0,1]

# loop over numbers of splines 
for i in range(0,4):
  
  # filter data 
  data_filtered2 = data[data.run == runs[i]]
  data_filtered2 = data_filtered.query('length_age4 == length_age4')

  # create predictor and target data frames 
  data_y = pd.DataFrame({
    'y':data_filtered2.length_age4
  })
  data_x = pd.DataFrame({
    'year':data_filtered2.brood_year -1970
  })
  print(len(data_x))
  # fit gam 
  gam = LinearGAM(s(0, n_splines = 10)).fit(data_x, data_y)

  # Plot the trend predicted by the modela and the confidence intervals
  XX = gam.generate_X_grid(term=0, n=200)
  print(len(XX))
  axs[fig_ind_x[i], fig_ind_y[i]].plot(XX, gam.predict(XX), 'r--')
  axs[fig_ind_x[i], fig_ind_y[i]].plot(XX, gam.prediction_intervals(XX, width=.95), color='b', ls='--')
  axs[fig_ind_x[i], fig_ind_y[i]].set_title(titles[i])

# x and y labels
for ax in axs.flat:
    ax.set(xlabel='Year', ylabel='length at age 4')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()


# In[ ]:


def init_clusters(n_clusters):
  # initialize each stock to a cluster at random
  for stock in data_filtered.stock:
    data_filtered.loc[data_filtered.stock == stock, 'cluster'] = np.random.randint(0,n_clusters)


# 

# In[ ]:


data_filtered['cluster'].value_counts()


# In[ ]:


all_min_errors = []
for iter in range(20):
  n_clusters = 3
  init_clusters(n_clusters)
  iterations = 15
  i=0;
  all_gams = {}
  total_err_list = [] # list to accumulate total MSE values
  while i<iterations:
    gams=[] #First GAM will be trained on cluster 0, second on cluster 1, third on cluster 2 data
    for c in range(n_clusters): 
      data_x_temp = pd.DataFrame({
          'year': data_filtered[data_filtered['cluster'] == c].brood_year - 1970
          })
      data_y_temp = pd.DataFrame({
          'y':data_filtered[data_filtered['cluster'] == c].length_age4
        })
      if (len(data_y_temp) == 0):
          init_clusters(n_clusters)
      print(data_y_temp)
      gam = LinearGAM(s(0, n_splines=10)).fit(data_x_temp, data_y_temp)
      gams.append(gam)
    all_gams[i] = gams;
    total_err = 0 # accumulates total error for each stock 
    for name, stockDf in data_filtered.groupby('stock'): #uses each stock dataframe
      x = np.array(stockDf.brood_year - 1970)
      y = np.array(stockDf.length_age4)
      mean_squared_errors = [] #indices indicate the cluster
      for cluster in range(n_clusters):
        y_prediction = np.array(gams[cluster].predict(x))
        MSE = np.sum(np.square(y - y_prediction))
        mean_squared_errors.append(MSE)

      min_err = min(mean_squared_errors)
      total_err += min_err # accumulate minimum error for each stock 
      
      assigned_cluster = mean_squared_errors.index(min_err) 

      data_filtered.loc[data_filtered.stock==name, 'cluster'] = assigned_cluster
    total_err_list.append(total_err) # add total error to list
    i+=1;
  all_min_errors.append(total_err)


# Notes from Jack:
# This all looks good, great work getting the algorithm up an running!
#
# It looks like most of what needs to be done is in place, but there are a few
# additional eatures that would help. 
# First, it would be great if we had  a metric that assessed the goodness of fit 
# of the model at each iteration.  For example, we could sum all of the MSE values
# calculated for each stock to get a total MSE value for each itteration. 
# W can then plot this value to see how and when teh model is converging. 
# It would also be good to experiment with differnt numbers of clusters, and differnt
# numbers of splines in the GAM to see how robust our results are to these parameters. 


# In[ ]:


all_min_errors


# In[ ]:


plt.scatter(np.arange(20),all_min_errors, color='r')
plt.grid()
plt.xticks(np.arange(20))
plt.yticks(np.linspace(1100000,1500000, 15))
plt.title('Run Iteration vs Least MSE')
plt.show()


# In[1]:


fig,axs = plt.subplots(15,3)
fig.set_figwidth(20)
fig.set_figheight(75)
for key,val in all_gams.items():
  i=0;
  for gam in val:
    x_plotted = gam.generate_X_grid(term=0, n=200)
    axs[key, i].plot(x_plotted, gam.predict(x_plotted), 'r--')
    axs[key, i].plot(x_plotted, gam.prediction_intervals(x_plotted, width=.95), color='b', ls='--')
    axs[key, i].set_title(f'Cluster:{i}, Iteration: {key+1}')
    axs[key, i].grid()
    i+=1


# The end goal will be to run unsupervised clustering techniques where we can learn what the best grouping of stocks may be. I will add some code that runs a simple implimentation of the EM algorithm, later in the week, 

# In[ ]:


# simple expectation maximization implimentation
'''
# set the number of clusters
n_clusters = 3
# initialize each stock to a cluster at random
for stock in data_filtered.stock:
  data_filtered.loc[data_filtered.stock == stock, 'cluster'] = np.random.randint(0,n_clusters)
# initialize loop
# data_x = pd.DataFrame({
#     'year':data_filtered.brood_year -1970
#   })
iterations = 5
i = 0
while i<iterations: 
#   # Expectation
    gams = {}
    gam_means = []
    #XX = gam.generate_X_grid(term=0, n=200)
    for c in range(n_clusters): #loop over clusters
      data_x_temp = pd.DataFrame({
          'year': data_filtered[data_filtered['cluster'] == c].brood_year - 1970

      })
      data_y_temp = pd.DataFrame({
        'y':data_filtered[data_filtered['cluster'] == c].length_age4
      }) 
      print(data_y_temp)
      gam = LinearGAM(s(0, n_splines=10)).fit(data_x_temp, data_y_temp) #fit (train) GAMs - the stock in each cluster assignment
      #x_interpolated = gam.generate_X_grid(term=0, n=200)
      gam_means.append(gam.predict(data_x_temp))
      gams[c] = gam   #save the GAM
#      
#   # Maximization
 
    stock_names = data_filtered.stock.unique()
    for name,stock_df in data_filtered.groupby('stock'):#loop over stocks
        data_stock_x = pd.DataFrame({
          'year': stock_df.brood_year - 1970
        })
        mse_vals = []    #for the current stock
        for c in range(n_clusters): #loop over clusters
           #print(stock_df.length_age4 - 1)
           #print(gam_means)
           MSE = sum(np.square((np.array(stock_df.length_age4)- gams[c].predict(data_stock_x) )))/len(stock_df.length_age4)  #compare all values for the stock to predicted values for the cluster (MSE)
           #print(MSE)
           mse_vals.append(MSE)    #save MSE values
        assigned_cluster = mse_vals.index(min(mse_vals))
        data_filtered.loc[data_filtered.stock == name, 'cluster'] = assigned_cluster
#
#     break loop over clusters 
#
#     Assign all data points for the stock to the cluster that describes the stock the best (lowest MSE)
    i+=1
# break loop when cluster assignemnts do not change
'''


# In[ ]:


'''
data_x_temp = pd.DataFrame({
   'year': data_filtered[data_filtered['cluster'] == 0].brood_year - 1970

})
data_y_temp = pd.DataFrame({
  'y':data_filtered[data_filtered['cluster'] == 0].length_age4
}) 
gam = LinearGAM(s(0, n_splines=10)).fit(data_x, data_y) #fit (train) GAMs - the stock in each cluster assignment
x_interpolated = gam.generate_X_grid(term=0, n=200)
#gam_means.append(gam.predict(x_interpolated))
#gams[0] = gam 
'''


# In[ ]:


'''
plt.plot(x_interpolated, gam.predict(x_interpolated), 'r--')
plt.plot(x_interpolated, gam.prediction_intervals(x_interpolated, width=.95), color='b', ls='--')
'''


# The algorithm above is fairly simple (not to say the implimentation will neccisarily be easy) and some elaborations can help improve its performance. To start I think we sould try to add some randoness to the algorithm, this will keep it from gettin gstuck at local maxima. This new stochastic implimentaion is described below. 

# In[ ]:


# stochastic expectation maximization implimentation

# initialize each stock to a cluster at random

# initialize loop

# Maximization
# fit GAMs the stock in each cluster assignment

# Expectation
# loop over the stocks
# evaluate the goodness of fit for each stock (MSE)
# assign to a cluster proportioanlly to the goodness of fit.
# e.g.  weights of softmax(-MSE)


# break loop when the nmber of itterations reaches a max value

