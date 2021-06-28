# Load Salmon growth data 
setwd("~/github/Chinook-Salmon-Research-Project")
dat = readRDS("raw_data/temp_dat.rds")
stock_characteristics <- read.csv("data/stock_characteristics_data_more_regions.csv")%>% dplyr::select(-stock)



dat_1 <- merge(dat,stock_characteristics, by = c("release_type","release_location_rmis_basin","run"))

dat_1 <- dat_1 %>% 
  dplyr::mutate(stock =paste(release_type,release_location_rmis_basin,run) )


dat_1 %>% dplyr::group_by(stock, age)%>%dplyr::summarize(n = n())


# restrict variables to stock, length, brood_year, age, fishery and sex where avaialble 
dat_2 <- dat_1 %>% 
  dplyr::select(stock, COG,recovery_day ,age, brood_year, release_type, release_age, length,length_type, fishery, gear)

dat_2$recovery_day <- scale(dat_2$recovery_day)


## get average lengths

dat_avg_2 <- dat_2 %>%
  dplyr::filter(age > 2|release_type=="one_YO_summer")%>%
  dplyr::group_by(stock,age,brood_year, release_type, COG)%>%
  dplyr::summarize(length = mean(length))#%>%
  #dplyr::select(-release_age)

### get length at age 1 and 2 from releases 

dat_age1 <- dat_1 %>% 
  dplyr::filter(!(is.na(avg_length)),
                avg_length < 350)%>% # removes one outlier
  dplyr::group_by(stock, brood_year, release_age, release_type, COG )%>%
  dplyr::summarize(length = mean(avg_length),
                   age = mean(release_age))%>%
  dplyr::select(-release_age)






# combine length data from releases and from recoveries 
dat_lengths <- rbind(dat_avg_2,dat_age1)


# make unique columns for each length at age 
dat_lengths_cast <- dat_lengths %>% reshape2::dcast(stock+brood_year+release_type+COG ~ age, 
                                                    value.var = "length")


# compute differnces between mean length at age 
dat_length_difs <- dat_lengths_cast %>% 
  dplyr::mutate(age_1_2 = `2`-`1`,
                age_2_3 = `3`-`2`,
                age_3_4 = `4`-`3`,
                age_4_5 = `5`-`4`,)

dat_length_difs_melt <- dat_length_difs %>%
  reshape2::melt(id.vars = c("stock","brood_year","release_type","COG"))






dat_GOA_fall <- dat_length_difs_melt %>%
  dplyr::filter(!(variable %in% c("1","2","3","4","5")),
                release_type == "one_YO_summer",
                COG > 47)%>%
  dplyr::filter(!(is.na(value)))

dat_NCC_fall <- dat_length_difs_melt %>%
  dplyr::filter(!(variable %in% c("1","2","3","4","5")),
                release_type == "one_YO_summer",
                COG < 47)%>%
  dplyr::filter(!(is.na(value)))

dat_spring <- dat_length_difs_melt %>%
  dplyr::filter(!(variable %in% c("1","2","3","4","5")),
                release_type == "two_YO_release")%>%
  dplyr::filter(!(is.na(value)))



# add years of growth increment - age when fish was observed
year <- c()
for(i in 1:nrow(dat_spring)){
  if(dat_spring$variable[i] == "age_1_2"){
    year <- append(year, dat_spring$brood_year[i]+2)
  }else if(dat_spring$variable[i] == "age_2_3"){
    year <- append(year, dat_spring$brood_year[i]+3)
  }else if(dat_spring$variable[i] == "age_3_4"){
    year <- append(year, dat_spring$brood_year[i]+4)
  }else if(dat_spring$variable[i] == "age_4_5"){
    year <- append(year, dat_spring$brood_year[i]+5)
  }
}
dat_spring$year <- year

year <- c()
for(i in 1:nrow(dat_NCC_fall)){
  if(dat_NCC_fall$variable[i] == "age_1_2"){
    year <- append(year, dat_NCC_fall$brood_year[i]+2)
  }else if(dat_NCC_fall$variable[i] == "age_2_3"){
    year <- append(year, dat_NCC_fall$brood_year[i]+3)
  }else if(dat_NCC_fall$variable[i] == "age_3_4"){
    year <- append(year, dat_NCC_fall$brood_year[i]+4)
  }else if(dat_NCC_fall$variable[i] == "age_4_5"){
    year <- append(year, dat_NCC_fall$brood_year[i]+5)
  }
}
dat_NCC_fall$year <- year


year <- c()
for(i in 1:nrow(dat_GOA_fall)){
  if(dat_GOA_fall$variable[i] == "age_1_2"){
    year <- append(year, dat_GOA_fall$brood_year[i]+2)
  }else if(dat_GOA_fall$variable[i] == "age_2_3"){
    year <- append(year, dat_GOA_fall$brood_year[i]+3)
  }else if(dat_GOA_fall$variable[i] == "age_3_4"){
    year <- append(year, dat_GOA_fall$brood_year[i]+4)
  }else if(dat_GOA_fall$variable[i] == "age_4_5"){
    year <- append(year, dat_GOA_fall$brood_year[i]+5)
  }
}
dat_GOA_fall$year <- year

# merge covariates

X <- read.csv("data/covariates.csv")

dat_GOA_fall <- merge(dat_GOA_fall,X,by = "year")
dat_NCC_fall <- merge(dat_NCC_fall,X,by = "year")
dat_spring <- merge(dat_spring,X,by = "year")




## finalize GOA fall data 
dat_GOA_fall_scaled <- dat_GOA_fall %>%
  dplyr::group_by( stock,variable)%>%
  dplyr::mutate(n = n())%>%
  dplyr::filter(n > 2)%>%
  dplyr::mutate(value = (value-mean(value))/sd(value))



dat_GOA_fall_scaled <- dat_GOA_fall_scaled %>%
  dplyr::select(year,stock,variable,value,SSTarc_summer,SSTarc_winter,PDO,
                WA_Pinks,ALPI,Pinks,NPGO,MEI_summer,MEI_winter, BI)


names(dat_GOA_fall_scaled) <- c("year","stock","variable","length","SSTarc_summer", "SSTarc_winter",
                                "PDO", "WA_Pinks","ALPI", "Pinks", "NPGO", "MEI_summer", "MEI_winter","BI")



dat_GOA_fall_age_1_2 <- dat_GOA_fall_scaled %>% 
  dplyr::filter(variable == "age_1_2") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)


dat_GOA_fall_age_2_3 <- dat_GOA_fall_scaled %>% 
  dplyr::filter(variable == "age_2_3") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)

dat_GOA_fall_age_3_4 <- dat_GOA_fall_scaled %>% 
  dplyr::filter(variable == "age_3_4") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)


dat_GOA_fall_age_4_5 <- dat_GOA_fall_scaled %>% 
  dplyr::filter(variable == "age_4_5") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)







## finalize NCCfall data 
dat_NCC_fall_scaled <- dat_NCC_fall %>%
  dplyr::group_by( stock,variable)%>%
  dplyr::mutate(n = n())%>%
  dplyr::filter(n > 2)%>%
  dplyr::mutate(value = (value-mean(value))/sd(value))



dat_NCC_fall_scaled <- dat_NCC_fall_scaled %>%
  dplyr::select(year,stock,variable,value,SSTarc_summer,SSTarc_winter,PDO,
                WA_Pinks,ALPI,Pinks,NPGO,MEI_summer,MEI_winter,BI)


names(dat_NCC_fall_scaled) <- c("year","stock","variable","length","SSTarc_summer", "SSTarc_winter",
                                "PDO", "WA_Pinks","ALPI", "Pinks", "NPGO", "MEI_summer", "MEI_winter","BI")



dat_NCC_fall_age_1_2 <- dat_NCC_fall_scaled %>% 
  dplyr::filter(variable == "age_1_2") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)


dat_NCC_fall_age_2_3 <- dat_NCC_fall_scaled %>% 
  dplyr::filter(variable == "age_2_3") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)

dat_NCC_fall_age_3_4 <- dat_NCC_fall_scaled %>% 
  dplyr::filter(variable == "age_3_4") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)


dat_NCC_fall_age_4_5 <- dat_NCC_fall_scaled %>% 
  dplyr::filter(variable == "age_4_5") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)




## finalize spring data 
dat_spring_scaled <- dat_spring %>%
  dplyr::group_by( stock,variable)%>%
  dplyr::mutate(n = n())%>%
  dplyr::filter(n > 2)%>%
  dplyr::mutate(value = (value-mean(value))/sd(value))



dat_spring_scaled <- dat_spring_scaled %>%
  dplyr::select(year,stock,variable,value,SSTarc_summer,SSTarc_winter,PDO,
                WA_Pinks,ALPI,Pinks,NPGO,MEI_summer,MEI_winter,BI)


names(dat_spring_scaled) <- c("year","stock","variable","length","SSTarc_summer", "SSTarc_winter",
                              "PDO", "WA_Pinks","ALPI", "Pinks", "NPGO", "MEI_summer", "MEI_winter","BI")




dat_spring_age_2_3 <- dat_NCC_fall_scaled %>% 
  dplyr::filter(variable == "age_2_3") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)

dat_spring_age_3_4 <- dat_NCC_fall_scaled %>% 
  dplyr::filter(variable == "age_3_4") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)


dat_spring_age_4_5 <- dat_NCC_fall_scaled %>% 
  dplyr::filter(variable == "age_4_5") %>%
  dplyr::ungroup()%>%
  dplyr::select(-variable)





## save data sets 


write.csv(dat_GOA_fall_age_1_2,"data/increments_GOA_fall_age_1_2.csv")
write.csv(dat_GOA_fall_age_2_3,"data/increments_GOA_fall_age_2_3.csv")
write.csv(dat_GOA_fall_age_3_4,"data/increments_GOA_fall_age_3_4.csv")
write.csv(dat_GOA_fall_age_4_5,"data/increments_GOA_fall_age_4_5.csv")

write.csv(dat_NCC_fall_age_1_2,"data/increments_NCC_fall_age_1_2.csv")
write.csv(dat_NCC_fall_age_2_3,"data/increments_NCC_fall_age_2_3.csv")
write.csv(dat_NCC_fall_age_3_4,"data/increments_NCC_fall_age_3_4.csv")
write.csv(dat_NCC_fall_age_4_5,"data/increments_NCC_fall_age_4_5.csv")


write.csv(dat_spring_age_2_3,"data/increments_spring_age_2_3.csv")
write.csv(dat_spring_age_3_4,"data/increments_spring_age_3_4.csv")
write.csv(dat_spring_age_4_5,"data/increments_spring_age_4_5.csv")






