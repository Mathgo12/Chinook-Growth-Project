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


## Some explanation/ background

The big picture question I want to work towards understanding with the simulation testing we are working on here is how well 
relationships  between biological processes that are importnat for conservation and resource management and physical and
climatological processes can be worked out using time series data. In principal we should be able to work out the relationship 
between these processes by analyzing correlations between the biological and the climatological processes. However, if the 
relationships are complex and the amount of data available is limited then there will be limits to the how well the true 
relationships can be reconstructed. These limitations will inevitably produce uncertainty and these uncertainties which are 
important to characterize. 

The goal of a simulation testing is precisely to characterize uncertainty. Our goal is to understand how well we the relationships 
between different processes can be understood, and how this is effected by our assumptions about the characteristics of the true 
underlying relationships and the quantities of data that are available. 

Simulation testing is a very useful method for answering these questions because we can simulate data sets where the true 
relationships are known. We can then use tools to try to reconstruct these relationships using the data that we simulated and 
compare the estimated relationships found by analyzing the data to the true relationships. Repeating this process many times on
many data sets will allow us to see how well and how consistently the true relationships used to generate the data can be 
reconstructed.

Three factors can influence uncertainty or our ability to extract information from a dat sets. The quality and quantity of the 
data, abstract characteristics of the true relationships, and the method used to estimate the relationships from the data. the
first factor, data  quantity and quality should be easy to understand. If there is more data it is easier to distinguish between
the true relationships in the data and correlations that simple appear by chance.  An example of "abstract characteristics of the 
true relationships" would be factors such as the strength of the true relationship and the functional form (e.g. linear or nonlinear).
These influence uncertainty because stronger relationships are easier to understand that weaker ones and simpler functional forms
such as linear relationships are easier to estimate than complex -nonlinear ones. The last factor, methedology can be quite important.
Some methods make strong assumptions about the true relationships, such as linearity. If these assumptions are violated then the method
will not beable to capture the true processes. In contrast other methods allow for more flexibility, but these methods are more likely
to "over fit" the data. We need to choose methods that make strong enough assumptions about the true relationships to avoid overfitting
without over simplifying. 


## Explanation of hyper-paramters for simulated data sets. 

Each of the data sets used for the simulation tests was generated to have distinct sets of characteristics. these characteristics are 
described by a set of "hyper paramters" the value of these paramters are saved in the hyper_params.csv files along side the data sets. These hyper paramters allow us to test how differnt factors effect the performance of the models we are testing change under differnt conditons. There are 9 differnt hyper paramters used to define the characteristics of the data sets n,	m,	total_effect,	nonlinear,	interactions,	rho_X,	int_X,	rho_U and int_U.

### n
the hyper paramter n describes the number of observaitons in the data set. 

### m 
the number of features used to generate the data

### total_effect. 
The amount of variability explained by the features. This can be thought of as the r squared value of a perfect model of the data set. 

### nonlinear

The number of nonlinear terms included in the model used to simulate the data. 

The sturcture of the model used to simualte the data is based on a linear regression model, e.g.

y = a + b*x1 + c*x2 + dx3 .

However, soe of the features are trasnfomed with a nonlinear function, e.g. 

y = a + b*x1 + c*x2 + d*f(x3) .

This hyper parmter decribes the number of features that have been transformed in this way.


### interacitons

This paramter describes the number of interaction terms included in the model.  

In addition to linear and nonlinear terms sometimes the product of two varibles is inculuded in the model, e.g.

y = a + b*x1 + c*x2 + d*x1*x2

This paramter describes how many of these terms ar eincluded in the model.

### rho_X, int_X

These paramters describe the distribution of the features (x varaibles)

### rho_U, int_U

These paramters describe the distribution of the variability in y that is not explained by the features (x). In other words they 
describe the distribtuion of the residuals of the perfrect model of the data. 




