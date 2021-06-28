# Regression Data

## Variables:

year:  year of coded wire tag (CWT) recovery

release_type: Describes the timing and size of the fish when released

run: describes the timing of the fishes return migration 

sex: male (M) or female (F)

release_location_rmis_basin:  describes the location that the fish was released from and is likely to return to.

release_location_rmis_region: describes the location that the fish was released from and is likely to return to, these have a coarser resolution than the basins. 

Age: age of the fish when the CWT was recovered

brood_year:  year when the fish hatched

fishery:  

gear:  gear used to capture fish 

release_age:  age when released 



## Time dependent data:

length: average length of fish with the given characteristics

release_length: size when released 

SSTarc_summer_lag(2,3,4):  a variable that describes the sea surface temperature in the east pacific two, three or four years prior. 

SSTarc_winter_lag(2,3,4):  a variable that describes the sea surface temperature in the east pacific two, three or four years prior. 

PDO_lag(2,3,4):  a variable that describes the climatological regime of the pacific ocean two, three or four years prior. 



NPGO_lag(2,3,4):  a variable that describes the climatological regime of the pacific ocean two, three or four years prior. 



Pinks_lag(2,3,4):  a variable that describes the abundance of pink salmon in the gulf of alaska two, three or four years prior. 

WA_Pinks_lag(2,3,4):  a variable that describes the abundance of pink salmon in the northern california current two, three and four years prior. 

ALPI_lag(2,3,4): a variable that describes the climatological regime of the Gulf of Alaska two, three or four years prior. 



## New data sets:

I added new data sets on 2/22/21:

regression_data_COWL_fall.csv
regression_data_COWL_spring.csv
regression_data_DESC_spring.csv
regression_data_YOCL_fall.csv

regression_data_fall_GOA.csv
regression_data_spring_GOA.csv
regression_data_fall_NCC.csv
regression_data_spring_NCC.csv

regression_data_mean_zero.csv


The first group of four data sets contain data for one stock each: Cowlitz river fall runs, Cowlitz river spring runs, Deschutes spring runs and =Youngs Bay fall runs. The second group of four data sets listed above contain data for the major run groupings: Fall run fish that migrate to the Gulf of Alaska (GOA), spring run fish that migrate to the Gulf of Alaska, and spring and fall run fish that migrate to the Northern California Current (NCC).  The last data set includes data for all of the stocks but the mean length for each stock is subtracted. 

Each data set has the same variables:

brood_year: 
The year prior to the observed fish’s first year of life. 

length:
The length of the fish from tip of the nose to fork of the tail

age:
Age when fish was measured

Run:
Life history characteristic of the fish:
1 - spring run
2 - summer run
3 - fall run
4 - late fall run

release_type:
A categorical variable that corresponds to the size and age when the fish was released from the hatchery.

Sex:
Male or female

p52.5
The proportion of marine catch for the stock of origin below 52.5 degrees latitude. This reflects the migratory behavior of the observed fish. 

Fishery and gear
How the fish was caught


## Environmental covariates: 

### Naming and time lags:

The other variables are environmental covariates. I changed the naming convention for these variables slightly the names should now read “**varaible name**_BY_**number of years since broodyear**”.  The number at the end corresponds to the age of the fish, so MEI_BY_3 would be the value of the multivariate el nino index  when the observed fish were 3 years old.

### Variables:

SSTarc.summer and SSTarc.winter

SST arc describes the sea surface temperature in the eastern pacific basin. High values indicate larger values of temperature. These values have increased overtime reflecting climate change. The tag .summer and .winter correspond to the season when the measurement was taken. 

PDO

This describes patterns of sea surface temperature in the north pacific ocean. These patterns correspond to changes in local conditions in the eastern pacific such as upwelling, which is a process whereby nutrients are brought up from deep waters to surface waters increasing productivity. 

WA_pinks

The size of the pink salmon population in washington

ALPI

Aleutian low pressure index. Describes interannual variability in atmospheric conditions over the north pacific, impacts the severity of storms, and sea surface temperature. 

Pinks

The size of the pink salmon population in the Gulf of Alaska

NPGO
Describes a pattern of sea surface temperature variability in the north pacific. This value is associated with the strength of currents flowing from the western to eastern pacific and like PDO corresponds to local scale ocean processes in the eatern pacific that impact productivity.

MEI

Multivariable el niño index describes el-niño oscillations. El-Nino describes variability in winds and currents in the tropical pacific. These variations impact the temperature and productivity of the california current. Prior work has shown that MEI impacts the length at age of chinook salmon form the sacramento river in california. 

BI

This index describes how currents flowing across the northpacific from east to west split when they get to the west coast of the United states. Typically these currents meet the coast near washington state and southern british columbia, but depending on the year will meet the coast further north or south. This variation changes where currents and correspondingly nutrients flow along the coast line.  
 









