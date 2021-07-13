#' simulating data sets with the form 
#' y = f(X) + U
#' where X is a vector f is a non-linear function and U is 
#' an unobsered process. The goal will be to generate models 
#' that can use a data set with values of y and X to reconstruct 
#' the function f. 
#' We will vary the the number of dimensions in X, the time series properties 
#' of X and U and the functinal form of f
#' 
#' The time series X and U are generted using the arima.sim function from 
#' the stats package, with differnt values for the AR and MA process. 
#' 
#' The functions f are composed of linear combinations of linear and sigmoidal
#' funcrions of the variable in X. Interacitons between variables are included
#' addively as linear or sigmidal funcions of the product of the interacting
#' variables. The sigmoidal function is chosen to add non-linear terms to the 
#' models because it can represent convex, saturating, and threshold responces
#' depending on the choice of parameters used.  


#' sigmoid(x,location,scale,height)
#' defines a nonlinear function of x with three parameters
sigmoid <- function(x, effect_size, location, scale ){
  x <- scale*(x-location)
  y <- exp(x)/(1+exp(x))
  y <- effect_size*(y-0.5)
  return(y)
}

#' draw_params(n, total_effect, nonlinear, interactions)
#' This function draws parameters for the function
#' f(X) = y used to create the siulation data sets
#' For each of the n variables in X it samples an effect
#' size from normal distribution such that the sum of 
#' squated effects equals total_effect. The arguments
#' nonlinear and interactions specify the number of variables
#' that have nonlinear effects and the number of interaction 
#' terms respectively. The varaibles with non-linear effects
#' and included in the interaction terms are sampled at random.
#' for each of the non-linear terms and additional two pramters
#' the locaiton and scale parmaters for the sigmiodal function 
#' are drawn. This function returns a data frame that saves 
#' the parameters used to build the function so it can be recreated. 
draw_params <- function(n, total_effect, nonlinear, interactions){
  # sample effects and scale so the sum of suared effects equals total_effect^2
  effect_sizes <- rnorm(n+interactions)
  f <- function(x) sum((x*effect_sizes)^2) - total_effect^2
  root <- uniroot(f, c(0, 10))
  x <- root$root
  effect_sizes <- x*effect_sizes

  # sample nonlinear terms
  if(nonlinear > 0){
    inds <- sample(1:n, nonlinear)
    location <- rnorm(nonlinear)
    scale <- rexp(nonlinear)
  }
  
  # sample interactions
  # first crate list with all sub sets of 1:n of size 2
  pairs <- list()
  for(i in 1:n){
    for(j in 1:n){
      if(i < j){
        pairs <- append(pairs, list(c(i,j)))
      }
    }
  }
  
  if(interactions > 0){
    terms <- sample(pairs, interactions)
  }
  
  #### put params in data frame
  variables <- 1:n
  interaction <- rep(NA, n)
  # add interactions
  if(interactions > 0){
    for(i in 1:interactions){
      variables <- append(variables, terms[[i]][1])
      interaction <- append(interaction, terms[[i]][2])
    }
  }
  
  locations <- rep(NA,n + interactions)
  scales <- rep(NA,n + interactions)
  if(nonlinear > 0){
    locations[inds] <- location
    scales[inds] <- scale
    nonlinear <- rep(F, n + interactions)
    nonlinear[inds] <- T
  }
  
  # add data to data frame
  pars <- data.frame(V1 = variables,
                     effect_size = effect_sizes, 
                     nonlinear = nonlinear,
                     location = locations,
                     scale = scales,
                     interactions = !(is.na(interaction)),
                     V2 = interaction)
  return(pars)
}


#' f(X,pars)
#' takes a vector X and a list if paramters genreated 
#' by draw_params and returns a value y
f <- function(X,pars){
  y <- 0
  for(i in 1:nrow(pars)){
    inter <- pars$interactions[i]
    nonlin <- pars$nonlinear[i]
    if(inter){
      ind1 <- pars$V1[i]
      ind2 <- pars$V2[i]
      B <- pars$effect_size[i]
      y <- y + B*X[ind1]*X[ind2]
    }else if(nonlin){
      ind <- pars$V1[i]
      effect_size <- pars$effect_size[i]
      location <- pars$location[i]
      scale <- pars$scale[i]
      y <- y + sigmoid(X[ind], effect_size, location, scale)
    }else{
      ind <- pars$V1[i]
      effect_size <- pars$effect_size[i]
      y <- y + effect_size * X[ind] 
    }
  }
  return(y)
}



