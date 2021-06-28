This file contains 11 data sets these data sets record the growth rates as measured by the difference between the average length of fish at age a and age a+1 in adjacent years. 

Each file set contains data for the growth increments in each year from 1979 to 2015, and a set of environmental predictors. Each file contains data for a different groups of stocks (spring, fall gulf of alaska, fall northern california current) and different ages. For example there is a file that contains all of the growth increments from age 2 to age 3 for spring run fish, and so on. The environmental variables are aligned so the measurement was taken in the year when the older age class of fish was observed. In other words the growth increment from 2 to 3 year old fish associated with the year 2000 is taken as the difference between 2 year old fish in 1999 and 3 year old fish in 2000. 


It would be great to start by fitting random forest models to each data set of the form:


Length = F(SSTarc_summer, SSTarc_winter, PDO, WA_pinks, Pinks, ALPI, NPGO, MEI_summer, MEI_winter) 

This can be done by creating a data set that only contains the length column and then a predictor set where the length, year, and stock variables are removed. 
