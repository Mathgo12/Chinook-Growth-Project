
library(dplyr)
library(rstan)
library(lubridate)
library(reshape2)
library(zoo)


setwd("~/github/Chinook-Salmon-Research-Project")
options(mc.cores = parallel::detectCores())


print("set working directory")


# useful function 
header.true.row.true <- function(df) {
  df$index <- rownames(df)
  names(df) <- as.character(unlist(df[1,]))
  df[-1,]
}


# define a function that extracts the years of data 
growth_years <- function(returns_data, min_age){
  df <- returns_data%>%
    group_by(age, brood_year, release_age)%>%
    dplyr::summarize(v = 1)
  years <- c()
  for(i in 1:nrow(df)){
    a <- df$age[i]
    ra <- df$release_age[1]
    for(age in min_age:(a)){ # subtract on for between age increments
      years <- append(years, df$brood_year[i] + age)
    }
  }
  return(list(years = sort(unique(years)),
              n_years = max(years) - min(years)+1, 
              off_set = min(returns_data$brood_year)+min_age - 1
  )
  )
}


# list for vaiables 
make_vars_ls <- function(num_vars, num_stocks){
  acc <- c()
  for(i in 1:num_vars){
    acc <- append(acc, rep(i, num_stocks))
  }
  return(acc)
}



###########################
###                     ###
###     Predictors      ###
###                     ###
###########################


print("defined functions")




# Pink Salmon Gulf of Alaska 


Pinks <- read.csv("raw_data/Pink_salmon.csv")
# organize pinks data 
Pinks <- Pinks%>%
  dplyr::mutate(Pink = as.numeric(Pink))%>%
  dplyr::filter(!(is.na(Pink)))
Pinks <- melt(Pinks, id.var = "Year")
Pinks <- Pinks%>%dplyr::group_by(variable)%>%dplyr::mutate(value = value/max(value))
Pinks <- Pinks %>% filter(variable == "Pink")

Pinks <- data.frame(year = Pinks$Year, Pinks = Pinks$value)
Pinks$Pinks <- scale(Pinks$Pinks)





print("alaska pinks")



# Pink Salmon Washington state 


salmon_abundance_WA <- read.csv("raw_data/WDFW-Salmonid_Stock_Inventory_Population_Escapement.csv")

d <- salmon_abundance_WA %>% 
  dplyr::filter(Species == "Pink",
                Data.Type == "Spawner Fish") 

even_year_value <- d %>% 
  dplyr::filter(!(is.na(Abundance.Quantity)), Year %% 2 == 0) %>% 
  dplyr::group_by(Year) %>% 
  dplyr::summarize(value = sum(Abundance.Quantity)) %>%
  dplyr::select(Year, value)
odd_year_value <- d %>% 
  dplyr::filter(!(is.na(Abundance.Quantity)), Year %% 2 == 1) %>% 
  dplyr::group_by(Year) %>% 
  dplyr::summarize(value = sum(Abundance.Quantity)) %>%
  dplyr::select(Year, value)

even_years <- even_year_value$Year
even_year_value1 <- even_year_value$value

missing_years <- data.frame(Year = seq(1960, 2020, 2)) %>% dplyr::filter(!(Year %in% even_years))
missing_values <- c()

for(i in 1:nrow(missing_years)){
  missing_values <- append(missing_values, sample(even_year_value1,1))
}


WA_Pinks <- rbind(odd_year_value,even_year_value,
                  missing_years %>% tibble::add_column(value = missing_values ) )


names(WA_Pinks) <- c("year", "WA_Pinks")

WA_Pinks$WA_Pinks <- scale(WA_Pinks$WA_Pinks)





print("washington prinks")




# Aleutian low pressure index

ALPI <- read.csv("raw_data/ALPI.csv")
names(ALPI) <- c("year","ALPI")
ALPI$ALPI <- scale(ALPI$ALPI)










# Pacific Decadal Oscilation

PDO <- read.csv("raw_data/PDO.csv")


PDO <- PDO%>%
  header.true.row.true()

names(PDO) <- c("Value","Date")


PDO <- PDO%>%
  dplyr::mutate(year = as.numeric(substr(Date,1,4)),
                month = as.numeric(substr(Date,5,6)))%>%
  dplyr::group_by(year)%>%
  dplyr::summarize(value = sum(as.numeric(Value))/n())

names(PDO) <- c("year", "PDO")


PDO$PDO <- scale(PDO$PDO)









# North Pacific Gyre Oscilations 

header.true <- function(df) {
  names(df) <- as.character(unlist(df[1,]))
  df[-1,]
}


NPGO <- read.csv("raw_data/NPGO.csv")

NPGO <- header.true(NPGO )

NPGO <- NPGO[c(2,3,4)]
names(NPGO) <- c("year", "month", "NPGO")


NPGO_data <- NPGO %>% dplyr::mutate(year = as.numeric(year),
                                    month = as.numeric(month),
                                    NPGO = as.numeric(NPGO))%>%
  
  dplyr::group_by(
    year
  )%>%
  dplyr::summarize(NPGO = mean(NPGO))%>%
  dplyr::ungroup()%>%
  dplyr::mutate(NPGO_5yr_rolling = zoo::rollapply(data = NPGO, 
                                                  width = 5, 
                                                  FUN = mean, 
                                                  align = "right", 
                                                  fill = NA, 
                                                  na.rm = T))






print("finished NPGO")


# North East Pacific Rim Sea Surface Tempreature 

# winter

SSTarc.winter <- read.csv("raw_data/ersstArc.win.csv")

SSTarc.winter <- SSTarc.winter%>%dplyr::mutate(
  rolling_5yr = rollapply(data = ersstArc.win, 
                          width = 5, 
                          FUN = mean, 
                          align = "right", 
                          fill = NA, 
                          na.rm = T))
names(SSTarc.winter) <- c("year", "SSTarc_winter", "SSTarc_winter_5yr_rolling") 


# summer 

SSTarc.summer <- read.csv("raw_data/ersstArc.sum.csv")

SSTarc.summer <- SSTarc.summer%>%dplyr::mutate(
  rolling_5yr = rollapply(data = ersstArc.sum, 
                          width = 5, 
                          FUN = mean, 
                          align = "right", 
                          fill = NA, 
                          na.rm = T))
names(SSTarc.summer) <- c("year", "SSTarc_summer", "SSTarc_summer_5yr_rolling") 


SSTarc.summer$SSTarc_summer <- scale(SSTarc.summer$SSTarc_summer)


### Columbia River Disharge Annual Averages ###


### Multivariate El-Nino index ###
MEI <- read.csv("raw_data/meiv2.csv")

MEI <- melt(MEI, id.var = "Year") 

seasons <- c()
for(i in 1:nrow(MEI)){
  if(MEI$variable[i] %in% c("X1", "X2", "X3")){
    seasons <- append(seasons, "winter")
  }
  if(MEI$variable[i] %in% c("X4", "X5", "X6")){
    seasons <- append(seasons, "spring")
  }
  if(MEI$variable[i] %in% c("X7", "X8", "X9")){
    seasons <- append(seasons, "summer")
  }
  if(MEI$variable[i] %in% c("X10", "X11", "X12")){
    seasons <- append(seasons, "fall")
  }
  
}

MEI$season <- seasons 

# spring
MEI_spring <-  MEI %>% 
  dplyr::group_by(season, Year) %>%
  dplyr::summarize(m = mean(value)) %>%
  dplyr::filter(season == "spring")


MEI_spring <- MEI_spring[,2:3]
names(MEI_spring) <- c("year", "MEI_spring")


# summer
MEI_summer <-  MEI %>% 
  dplyr::group_by(season, Year) %>%
  dplyr::summarize(m = mean(value)) %>%
  dplyr::filter(season == "summer")


MEI_summer <- MEI_summer[,2:3]
names(MEI_summer) <- c("year", "MEI_summer")


### Bifrucation index ###

BI <- read.csv("raw_data/BI.csv") %>% 
  header.true.row.true() %>% 
  dplyr::select(year, bifurcation_index)

names(BI) <- c("year", "BI")
BI$BI <- as.numeric(BI$BI)
### total hatchery releases ###


# Arrange all covariates into a data frame 

df_list <-  list(SSTarc.summer, 
                 SSTarc.winter, 
                 PDO,
                 WA_Pinks,
                 ALPI,
                 Pinks,
                 NPGO_data,
                 MEI_spring,
                 MEI_summer,
                 BI
)


f <- function(d1, d2){ merge(d1, d2, by = "year")}
covriates <- Reduce(f, df_list)


X <- covriates %>% select(year,
                          SSTarc_summer,
                          SSTarc_winter,
                          PDO,
                          WA_Pinks,
                          ALPI,
                          Pinks,
                          NPGO,
                          MEI_summer,
                          BI)



##############################
###                        ###
###   salmon growth data   ###
###                        ###
##############################


# Salmon growth data 
dat = readRDS("raw_data/temp_dat.rds")



# filter out ages and run types that are not helpful
dat1 = dplyr::filter(dat, 
                     release_location_rmis_region %in% c("LOCR", "CECR", "UPCR", "SNAK"),
                     run %in% c(1,2,3,8),
                     sex %in% c("M","F"), 
                     age > 2)

# filter out brood years w/ very few stocks 
dat1 <- dat1%>%filter(brood_year > 1980, recovery_year < 2012)



release_lengths <- dat1%>% 
  filter(sex %in% c("M","F"),!(is.na(run)),!(is.na(release_type))  )%>%
  group_by(release_type, run, sex)%>%
  dplyr::summarize(release_length = sum(avg_length,na.rm=TRUE)/sum(!(is.na(avg_length))))




# filter outsotck year combinations with fewer than 25 observations
min_obs <- 10
dat1 = dat1 %>%
  dplyr::group_by(sex,run,release_location_rmis_basin, release_location_rmis_region, release_type, age, brood_year) %>% 
  dplyr::mutate(n = n()) %>%
  dplyr::filter(n > min_obs)

# fileter out stocks with fewer than ten years of observations for at least one age 
min_yrs <- 15
dat1 = dat1 %>%
  dplyr::group_by(sex,run,release_location_rmis_basin, release_location_rmis_region, release_type, age) %>% 
  dplyr::mutate(nyears = length(unique(brood_year))) %>%
  dplyr::filter(nyears > min_yrs)


# filter out stocks with fewer than two ages with sufficent observations
min_ages <- 1
dat1 = dat1 %>%
  dplyr::group_by(sex,run,release_location_rmis_basin, release_location_rmis_region, release_type) %>% 
  dplyr::mutate(nages = length(unique(age))) %>%
  dplyr::filter(nages > min_ages)



dat_means <- dat1 %>% 
  dplyr::group_by(release_type, run, sex, release_location_rmis_basin, release_location_rmis_region, age, brood_year, fishery, gear, release_age) %>%
  dplyr::summarize( length = mean(length), 
                    y_n = n())





dat_means <- merge(dat_means, release_lengths, by = c("release_type", "run", "sex"))

# filter out fisheires are gear types with too few observaitons 
min_obs <- 50
dat_means = dat_means %>% 
  dplyr::mutate(fishery_gear = paste0(fishery,":",gear)) %>% 
  dplyr::group_by(fishery_gear) %>% 
  dplyr::mutate(n = n()) %>%
  dplyr::filter(n > min_obs)%>%
  dplyr::ungroup()


dat_means <- dat_means%>%
  dplyr::mutate(stock = paste(release_type, ";", run, ";", sex, ";", release_location_rmis_basin),
                fishery_gear = paste(fishery, ";", gear))





### add ocean distribution data ####

stock_characteristics <- read.csv("samples/stock_characteristics_data.csv")%>% dplyr::select(-stock)


data_means <- merge(dat_means, stock_characteristics, by = 
                      c("run", "release_type", "sex", "release_location_rmis_basin"))



dat_means <- data_means %>% mutate(marine_dsn = (run == 3 & p52.5 < 0.95)) %>%
  mutate(group = paste(run, ";", marine_dsn))




dat_means$group <- as.numeric(as.factor(dat_means$group))












### remove means from each population ###






### lag data set
X_BY_0 <- X %>% dplyr::mutate(year = year + 1)
names(X_BY_0) <- c("brood_year", "SSTarc.summer_BY_1", "SSTarc.winter_BY_1", "PDO_BY_1",
                   "WA_Pinks_BY_1",  "ALPI_BY_1", "Pinks_BY_1", "NPGO_BY_1",
                   "MEI_BY_1", "BI_BY_1")

X_BY_1 <- X %>% dplyr::mutate(year = year + 2)
names(X_BY_1) <- c("brood_year", "SSTarc.summer_BY_2", "SSTarc.winter_BY_2", "PDO_BY_2",
                   "WA_Pinks_BY_2",  "ALPI_BY_2", "Pinks_BY_2", "NPGO_BY_2",
                   "MEI_BY_2", "BI_BY_2")


X_BY_2 <- X %>% dplyr::mutate(year = year + 3)
names(X_BY_2) <- c("brood_year", "SSTarc.summer_BY_3", "SSTarc.winter_BY_3", "PDO_BY_3",
                   "WA_Pinks_BY_3",  "ALPI_BY_3", "Pinks_BY_3", "NPGO_BY_3",
                   "MEI_BY_3", "BI_BY_3")


X_BY_3 <- X %>% dplyr::mutate(year = year + 4)
names(X_BY_3) <- c("brood_year", "SSTarc.summer_BY_4", "SSTarc.winter_BY_4", "PDO_BY_4",
                   "WA_Pinks_BY_4",  "ALPI_BY_4", "Pinks_BY_4", "NPGO_BY_4",
                   "MEI_BY_4", "BI_BY_4")



dat_mean_zero <- dat_means %>% 
  dplyr::group_by(run, age, sex, release_type, release_location_rmis_basin) %>%
  dplyr::mutate(m_length = mean(length),
                sd_length = sd(length))%>%
  dplyr::ungroup()%>%
  dplyr::mutate(length = (length - m_length)/sd_length) %>% 
  select(length,
         brood_year,
         age,
         run, 
         release_type, 
         sex,
         p52.5,
         fishery,
         gear) %>% 
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year")


write.csv(dat_mean_zero, "data/regression_data_mean_zero.csv")




### grouped observations ####

dat_means_grouped <- dat_means %>% 
  select(length,
         brood_year,
         age,
         run, 
         release_type, 
         sex,
         p52.5,
         fishery,
         gear,
         stock)


### fall gulf of alaska
dat_means_fall_GOA <- dat_means_grouped %>%
  dplyr::filter(release_type == "one_YO_summer",
                run %in% c(3,8),
                p52.5 < 0.95)


dat_means_fall_GOA <- dat_means_fall_GOA %>%
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year")

dat_means_fall_GOA <- dat_means_fall_GOA %>% 
  dplyr::select(-stock)

write.csv(dat_means_fall_GOA, "data/regression_data_fall_GOA.csv")

### fall northern california current
dat_means_fall_NCC <- dat_means_grouped %>%
  dplyr::filter(release_type == "one_YO_summer",
                run %in% c(3,8),
                p52.5 >0.95)


dat_means_fall_NCC <- dat_means_fall_NCC %>%
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year")

dat_means_fall_NCC <- dat_means_fall_NCC %>% 
  dplyr::select(-stock)

write.csv(dat_means_fall_NCC, "data/regression_data_fall_NCC.csv")




### spring gulf of alaska
dat_means_spring_GOA <- dat_means_grouped %>%
  dplyr::filter(release_type == "two_YO_release",
                run %in% c(1,2),
                p52.5 <0.95)


dat_means_spring_GOA <- dat_means_spring_GOA %>%
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year")

dat_means_spring_GOA <- dat_means_spring_GOA %>% 
  dplyr::select(-stock)

write.csv(dat_means_spring_GOA, "data/regression_data_spring_GOA.csv")


### spring northern california current
dat_means_spring_NCC <- dat_means_grouped %>%
  dplyr::filter(release_type == "two_YO_release",
                run %in% c(1,2),
                p52.5 <0.95)


dat_means_spring_NCC <- dat_means_spring_NCC %>%
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year")

dat_means_spring_NCC <- dat_means_spring_NCC 
write.csv(dat_means_spring_NCC, "data/regression_data_spring_NCC.csv")




### select populaitons 

# fall
dat_means_stocks = dat_means_grouped %>%
  dplyr::group_by(stock) %>% 
  dplyr::mutate(nyears = length(unique(brood_year))) 

dat_means_fall <- dat_means_stocks %>%
  dplyr::filter(run == 3)


dat_means_COWL_fall <- dat_means_fall %>%
  dplyr::filter(stock %in% c("one_YO_summer ; 3 ; F ; COWL",
                             "one_YO_summer ; 3 ; M ; COWL"))


dat_means_COWL_fall <- dat_means_COWL_fall %>%
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year") %>%
  select(-nyears)

write.csv(dat_means_COWL_fall, "data/regression_data_COWL_fall.csv")

dat_means_YOCL_fall <- dat_means_fall %>%
  dplyr::filter(stock %in% c("one_YO_summer ; 3 ; F ; YOCL",
                             "one_YO_summer ; 3 ; M ; YOCL"))


dat_means_YOCL_fall <- dat_means_YOCL_fall %>%
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year") %>%
  select(-nyears)

write.csv(dat_means_YOCL_fall, "data/regression_data_YOCL_fall.csv")

# spring

dat_means_stocks = dat_means_grouped %>%
  dplyr::group_by(stock) %>% 
  dplyr::mutate(nyears = length(unique(brood_year))) 




dat_means_spring <- dat_means_stocks %>%
  dplyr::filter(run == 1)

d <- dat_means_spring %>% dplyr::filter(nyears == 26)

dat_means_DESC_spring <- dat_means_spring %>%
  dplyr::filter(stock %in% c("two_YO_release ; 1 ; M ; DESC",
                             "two_YO_release ; 1 ; F ; DESC"))

dat_means_DESC_spring <- dat_means_DESC_spring %>%
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year") %>%
  select(-nyears)

write.csv(dat_means_DESC_spring, "data/regression_data_DESC_spring.csv")


dat_means_COWL_spring <- dat_means_spring %>%
  dplyr::filter(stock %in% c("two_YO_release ; 1 ; M ; COWL",
                             "two_YO_release ; 1 ; F ; COWL"))

dat_means_COWL_spring <- dat_means_COWL_spring %>%
  merge(X_BY_0, by = "brood_year") %>%
  merge(X_BY_1, by = "brood_year") %>%
  merge(X_BY_2, by = "brood_year") %>%
  merge(X_BY_3, by = "brood_year")%>%
  select(-nyears)

write.csv(dat_means_COWL_spring, "data/regression_data_COWL_spring.csv")

