setwd("~/github/Chinook-Growth-Project")
library(ggplot2)
library(dplyr)
library(PNWColors)
dat <- read.csv("main/sim_results_4.csv")

dat <- reshape2::melt(dat, id.vars = names(dat)[c(1,2,5,6,7,8,9,10,11,12)])
head(dat)

# plot cos_sim scores as a function of ech variable 
ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(N), y = value, fill = variable))+
  geom_boxplot()+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))

ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(totals_effect), y = value, fill = variable))+
  geom_boxplot()+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))


ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(interactions), y = value, fill = variable))+
  geom_boxplot()+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))
  

ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(nonlinear), y = value, fill = variable))+
  geom_boxplot()+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))


ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(features), y = value, fill = variable))+
  geom_boxplot()+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))


ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(rho_X), y = value, fill = variable))+
  geom_boxplot()+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))


ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(rho_U), y = value, fill = variable))+
  geom_boxplot()+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))




ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(nonlinear), y = value, fill = variable))+
  geom_boxplot()+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))


# do the models perform better with non-linearities and 
# interaction with more data?

ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(nonlinear), y = value, fill = variable))+
  geom_boxplot()+
  facet_wrap(~N, ncol = 3)+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))

ggplot(dat %>% filter(variable %in%c("cos_sim", "cos_sim_rand")), 
       aes(x = as.factor(interactions), y = value, fill = variable))+
  geom_boxplot()+
  facet_wrap(~N, ncol = 3)+
  theme_classic()+
  scale_fill_manual(values = pnw_palette("Cascades",2))


dat <- read.csv("main/sim_results_4.csv")

## plot the correlation betwen R2 train and cos_sim
ggplot(dat,
       aes(x = r2_train, y = cos_sim, 
           color = as.factor(paste(N,totals_effect))))+
  geom_point()+
  facet_grid(N~totals_effect)+
  geom_smooth(method = "lm")

## plot the correlation betwen R2 test and cos_sim
ggplot(dat %>% filter(r2_test > -1),
       aes(x = r2_test, y = cos_sim, 
           color = as.factor(paste(N,totals_effect))))+
  geom_point()+
  facet_grid(N~totals_effect)+
  geom_smooth(method = "lm")



