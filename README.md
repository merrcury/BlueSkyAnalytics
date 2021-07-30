# BlueSky Analytics Assignment 

## Assignment - 1 

URL : http://ec2-65-2-5-130.ap-south-1.compute.amazonaws.com/

### Following Name Conversions have been used. 

| Long Name                                                                                                        | Short Name  |
|------------------------------------------------------------------------------------------------------------------|-------------|
| carbon_dioxide_co2_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent    | CO2         |
| 'greenhouse_gas_ghgs_emissions_including_indirect_co2_without_lulucf_in_kilotonne_co2_equivalent'                | GHG-CO2     |
| 'greenhouse_gas_ghgs_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent' | GHG         |
| 'hydrofluorocarbons_hfcs_emissions_in_kilotonne_co2_equivalent'                                                  | HFC         |
| 'methane_ch4_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent'         | CH4         |
| 'nitrogen_trifluoride_nf3_emissions_in_kilotonne_co2_equivalent'                                                 | HF3         |
| 'nitrous_oxide_n2o_emissions_without_land_use_land_use_change_and_forestry_lulucf_in_kilotonne_co2_equivalent'   | N2Os        |
| 'perfluorocarbons_pfcs_emissions_in_kilotonne_co2_equivalent'                                                    | PFCs        |
| 'sulphur_hexafluoride_sf6_emissions_in_kilotonne_co2_equivalent'                                                 | SF6         |
| 'unspecified_mix_of_hydrofluorocarbons_hfcs_and_perfluorocarbons_pfcs_emissions_in_kilotonne_co2_equivalent'     | HFC-PFC-mix |

### Important Links

Swagger Documentation Located at -> http://ec2-65-2-5-130.ap-south-1.compute.amazonaws.com/

Redoc Documentation Located at -> http://ec2-65-2-5-130.ap-south-1.compute.amazonaws.com/redoc

OpenAPI JSON -> http://ec2-65-2-5-130.ap-south-1.compute.amazonaws.com/api/v0.1.0/openapi.json


### Task Completed 

- [X] /countries - get all countries in the dataset (names, ids and their possible values for startYear and endYear)
- [X] /country/id?queries=explained-below
     - [X] temporal queries - startYear | endYear
     - [X] parameters queries - one or parameters (e.g, CO2 or CO2 and NO2)
     - [X] should return all values for the selected parameters between startYear and endYear
- [X] Add appropriate checks for queries and erroneous values (Checks Implemented). 
     - [X] Required Fields in Route 2
     - [X] Type Check of fields in Route 2
     - [X] Upper Bound and Lower both for all Country ID, Start Year and End Year
     - [X] End Year cannot be smaller than Start Year 
- [X] Bonus Features:
     - [X] Add caching (using Redis) 

### Questionnaire

1. What was the most challenging part?

   Parsing single parameter for `category`. I was using tuple earlier and single tuple stores as ("CO2",). It
   came with extra comma and SQL Syntax Fails on same. 

2. What was the most fun part?

   Tackling `category` parameter and again end up using tuple only. Other One I would say is setting all MySQL, Redis
   and Code in EC2 instance. 
   
3. What do you think is wrong with this task or could be made better in this task?

   There was no technical blocker with the task. But definitely, Some addition can be made like YoY increase of Gas,
   Comparison between two gases in the same country, Comparison of One Country to another. 
   
### Screenshots

1. Route -> /countries
![Get ID](/images/getid.png)

2. Route -> /country/id 
![Get Data](/images/getdata.png)

### Technical Specifications 
+ Python 3.7 
+ MySQL 8.0 
+ Redis 6.2 

