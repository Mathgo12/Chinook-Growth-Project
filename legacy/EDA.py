#!/usr/bin/env python
# coding: utf-8

# #Exploritory data analysis for Chinook growth unsupervised learning project
# 
# This notebook is for creating simple plots and graphics to help produce a general understanding for the patterns and trends in the growth data set
# 

# In[ ]:


# importing data
import pandas as pd
means_stock=pd.read_csv('data/dat_means_stock.csv')
means_stock


# In[ ]:


# plotting time series
# I am using pandas for this plot but feel free to use what ever package your
# are most familiar with. I do not use Python for plotting (I ususally use R
# for this) so I probably i wll not be able to help too much if you run into 
# issues but there are lots of resources on stack exchange, and I am happy 
# to take a look if an issues arises. 

means_stock.plot(x = "brood_year",
        y = "length", 
        kind = 'scatter', 
        c = "age",
        colormap='viridis',
        alpha = 0.5)

