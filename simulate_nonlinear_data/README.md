# Simulation testing

## General notes
This directory contains code that generated data sets similar to the chinook growth data set but there are known
relationships between the predictors and the dependent variable. These data sets can be used to test how well a chosen
methedology is able to identify relationships between variable sin the real data set, and how its performance might change
if more (or less) data eas available. 

## next steps
So far we have writen code to generate data set and to fit random forest models to those data. The next step is to 
compare the relationships that the random forest model found between in the data set to the true relationships used to 
to simulate them. 

One metric that is often used to interperet random forest models are variable importance scores. To start we can compare 
the scores produced by the model to the importance of each variable used to generate the simulated data sets. For each of the
data sets there is a file labeled "par.csv" htat describes the paramters used in the model that generated the data set. These
files have a column labeled "effect_size" the square of this quantity can be used as a measure of varible importnace. There are 
some additional consideration that need to be taken into account becuase the models include interacitons between the vairables
and non-linearities. To handle these issues I wrote a function in the "compute_importance.R" file. Running this file writes a file
names "Imp.csv" to each of the directories contiantin a simulated data set. 

The next step will be to write a program that compares the true importnace valeus stored in the "Imp.csv" files to the importance 
values produced by the random forest models. The exact numerical value of importnace will not be directly comparable, but the 
the reletive ordering of the variables will be. 

We need to write code that fits a random forest model to each of the data sets and returns the reletive ranking of the variables.

Next we need to compare this ranking to the true values stored in the "Imp.csv" files. 

These comparisons should be summarized by a single value that describes how similar the values are. We can then make plots that show 
how this performance metric changes has each of the hyper paramters used to genreate the data sets are changed.





