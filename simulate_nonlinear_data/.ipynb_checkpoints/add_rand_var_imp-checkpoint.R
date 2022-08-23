
setwd("~/github/Chinook-Growth-Project")

generate_var_importance <- function(n){
  effect_sizes <- rnorm(n)
  f <- function(x) sum((x*effect_sizes)^2) - 0.75
  root <- uniroot(f, c(0, 100))
  x <- root$root
  effect_sizes <- x*effect_sizes
  return(effect_sizes^2)
}


dat <- read.csv("simulate_nonlinear_data/data_set_39/Imp.csv")
n <- nrow(dat)
rand <- generate_var_importance(n)
dat$rand <- rand
dat
for(i in 1:1000){
  path <- paste("simulate_nonlinear_data/data_set_",
                i,"/Imp.csv",sep = "")
  dat <- read.csv(path)
  n <- nrow(dat)
  rand <- generate_var_importance(n)
  dat$rand <- rand
  write.csv(dat,path)
}
