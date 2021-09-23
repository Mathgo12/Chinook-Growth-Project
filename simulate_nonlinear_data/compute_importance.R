library(dplyr)

setwd("~/github/Chinook-Growth-Project")
pars <- read.csv("simulate_nonlinear_data/test/par.csv")

compute_importance <- function(j){
  dat <- read.csv(paste("simulate_nonlinear_data/data_set_",j,"/par.csv",sep = ""))
  print(dat)
  impvals <- rep(0,20)
  
  for(i in 1:nrow(dat)){
    if(is.na(dat$V2[i])){
      impvals[dat$V1[i]] <- impvals[dat$V1[i]] + dat$effect_size[i]^2
    }else{
      impvals[dat$V1[i]] <- impvals[dat$V1[i]] + abs(dat$effect_size[i])
      impvals[dat$V2[i]] <- impvals[dat$V2[i]] + abs(dat$effect_size[i])
    }
  }
  
  impvals <- impvals[impvals != 0]
  print(impvals)
  dat <- data.frame(V = 1:length(impvals), Imp = impvals)
  print(dat)
  write.csv(dat,paste("simulate_nonlinear_data/data_set_",j,"/Imp.csv",sep = ""))
}

#compute_importance(3)
parallel::mclapply(1:600,compute_importance, mc.cores = 10)