@data/sunday_unified_geo_data_rows.csv  contains temporal data as well for illegal sand mining. as mining observation data is less reliable temporally, @data/no_mobs_unified_geo_data_rows.csv  has all verified reliable temporal data for sand mining. The presence of temporal data now means we can do a LOT more analysis. You can choose to REDO a SUBSET of existing analyses done already in this workspace if you think we'll get statistically significant results.

Now onto the NEW datasets. For all of these, you will need to load and clean the data with pandas. Dates may be in string form and irregular, so inspect before applying any cleaning rules. Pay attention to the years in which this data was recorded. If the date recorded is irrelevant/not consistent with illegal sand mining temporal data -- only do SPATIAL analysis. It is up to you to preserve correctness with your analytical decisionmaking.

Add to our @spatial_analysis.ipynb notebook with the ENVIRONMENT datasets:
@data/env/water/ganga.csv  and @data/env/water/sangam.csv contain more river quality data observations over time for the rivers ganga and sangam.

For these, create a new notebook and do in-depth analysis of whether construction and housing projects (ie, sand demand) correlated with increased illegal sand mining (ie, sand supply). Beyond correlation, apply similar and advanced spatial analysis tools to understand (1) distance from construction/sand demand to mining sites and (2) clusters of construction and clusters of sand mining. Then go above and beyond everything i told you to get research-grade results from these datasets and learn more about illegal sand mining. We want to really understand the connection between housing, construction and illegal sand mining on multiple dimensions.

CONSTRUCTION DATASETS FROM DATA.GOV.IN

State/UT-wise Details of Houses Sanctioned and Construction Cost to be spent under Pradhan Mantri Awas Yojana-Urban (PMAY-U) as on 20-11-2023
@data/construction_housing/UP_districtwise_PMAY_2025.csv 

District-wise Details of Houses Sanctioned, Grounded for Construction and Completed/Delivered for the Beneficiaries under Pradhan Mantri Awas Yojana - Urban (PMAY-U) in the State of Uttar Pradesh during 2022-23 and 2023-24
 @data/construction_housing/UP_districtwise_PMAY_2023_24_and_2024_25.csv 

 State/UT-wise Details of Houses Sanctioned and Construction Cost to be spent under Pradhan Mantri Awas Yojana-Urban (PMAY-U) as on 20-11-2023

@data/construction_housing/statewise_PMAY_constructioncost_sanctionedhouses2013.csv 

 State/UT-wise Details of Houses Sanctioned, Grounded for Construction and Completed/Delivered under Pradhan Mantri Awas Yojana- Urban (PMAY-U) (In Reply to Unstarred Question on 04-12-2023)
@data/construction_housing/statewise_PMAY_constructioncost_sanctionedhouses_actualbuilt.csv 

 State/UT-wise Details of Houses Sanctioned, Grounded for Construction and Completed/Delivered under Pradhan Mantri Awas Yojana-Urban (PMAY-U) from 2018-19 to 2023-24

@data/construction_housing/state_sanctioned_PMAY_houses_construction_2018_to_2024.csv 

Illegal sand mining is likely caused by economic factors like poverty/unavailability of other jobs/literacy and urbanisation (which links with construction). Suggest and then carry out ADVANCED in-depth STATISTICAL and SPATIAL techniques to uncover patterns betweeen economic factors and illegal sand mining:

ECONOMIC DATASETS
State-wise literacy rate 
@data/economics_urbanisation/literacy_rate_statewise.csv
it's years are in a string and need to be extracted/cleaned as datetime/year field

Percentage of population below the poverty line state-wise for India
@data/economics_urbanisation/percent_bpl_statewise.csv  

Urban populations in each state
@data/economics_urbanisation/urban_population_statewise.csv