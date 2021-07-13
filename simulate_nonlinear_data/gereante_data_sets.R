source("~/documents/simulate_nonlinear_data/function_sim.R")
source("~/documents/simulate_nonlinear_data/time_series_sim.R")


#' generate_data_set(dir,n, m, total_effect, nonlinear, interactions, rho_X, rho_U) 
#' generates a data set of length n with m covariates
#' that explain total_effect < 1 percent of the variance
#' the rest of the varinace is explained by a time seires
#' with autocorelation coeficents given by rho_U
#' the numbe rof nonlinear and interaction terms are
#' specified by nonlinear, interactions
#' the function returns a 1 by n matrix of y values
#' a m by n matrix of X values and a data frame "pars"
#' that specifies the relationship between y and X
#' these values are saved in a directory specifed by path
#' dir, along with the matrices rho_X and rho_U used to genrate 
#' the data. 
generate_data_set <- function(dir,
                              n, m, 
                              total_effect, nonlinear, interactions, 
                              rho_X, rho_U){
  dir.create(dir)
  hyper_params <- data.frame(
    n = n, m = m, total_effect = total_effect,
    nonlinear = nonlinear, interactions = interactions,
    rho_X = rho_X[[1]][1], int_X = length(rho_X[[1]]), rho_U = rho_U[1], 
    int_U = length(rho_U) 
  )
  write.csv(hyper_params,paste(dir, "/hyper_params.csv",sep = "") )
  par <- draw_params(m,total_effect, nonlinear, interactions) 
  X <- generate_X(n,m,rho_X)
  U <- generate_X(n,1,rho_U)
  U <- (1-total_effect)*U
  f_i <- function(x) f(x,par)
  y <- apply(X,MARGIN = 1, FUN = f_i)
  y <- y + U
  y <- (y - mean(y))/sd(y)
  write.csv(X, paste(dir, "/X.csv",sep = ""))
  write.csv(y, paste(dir, "/y.csv",sep = ""))
  write.csv(U, paste(dir, "/U.csv",sep = ""))
  write.csv(par, paste(dir, "/par.csv",sep = ""))
  write.csv(rho_X, paste(dir, "/rho_X.csv",sep = ""))
  write.csv(rho_U, paste(dir, "/rho_U.csv",sep = ""))
  
}



##### run simulations

n_ls <- c(30,50,100)
m_ls <- c(2,5,10)
total_effect_ls <- c(0.25,0.5,0.75)
non_linear_ls <- c(0,1,3) # m 
interactions_ls <- c(0,1,2) # #m/2*(m-1)
rho_X_ls <- list(c(0.0,0.0), c(0.5,0.0), c(0.5,0.5))
rho_U_ls <- list(c(0.0,0.0), c(0.5,0.0), c(0.5,0.5))
i <- 0
while(i < 100){
  
  n = sample(n_ls,1)
  m = sample(m_ls,1)
  total_effect = sample(total_effect_ls,1)
  non_linear = sample(non_linear_ls, 1)
  interactions = sample(interactions_ls, 1)
  rho_X = sample(rho_X_ls,1)[[1]]
  rho_U = sample(rho_U_ls,1)[[1]]
  rho_U <- matrix(rho_U[[1]], ncol = 2, nrow = 1)
  rx <- rho_X
  for(j in 1:m-1){
    rho_X <-  rbind(rho_X,rx)
  }
  if(m > non_linear & interactions  < m){
    i <- i + 1
    generate_data_set(paste("~/documents/simulate_nonlinear_data/data_set_",i, sep = ""), n, m, 
                     total_effect, non_linear , interactions, 
                    rho_X, rho_U)
  }
}

generate_data_set("~/documents/simulate_nonlinear_data/test", 30, 2, 
                              0.5, 0, 0, 
                              rbind(c(0.5,0.5),c(0.5,0)), as.matrix(c(0.5,0)))












