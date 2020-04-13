# HCQ_US_COVID19
Calculations using IHME Data for Hydroxychloroquine (HCQ) needs for COVID-19 in US.

Depends on:
numpy, pandas and matplotlib

Includes rationale, some examples of how policy can be improved and comparison of death rates to Marseilles, France with respect to using this generic drug

Answers three questions:
What will the US hydroxychloroquine needs be for solving COVID-19 assuming nearly complete shelter in place?
What is the supply?
What will it cost?

The IHME data was downloaded from http://healthdata.org/covid and is changed every 2-3 days as new data is incoming.
The infection rate used was inferred by using the current death rate as work began on the original blog post which stood at
12,936/401,166 = 0.032246 (source https://www.cnn.com/interactive/2020/health/coronavirus-us-maps-and-cases/)

Conclusions for 3 questions posed:
1. ~15M 200mg HCQ pills will be neeed
2. >40M HCQ pills will be supplied
3. <$3M 

Description
medium_HCQblogpost.py: graph plotting and analysis script
IHME_USA_Proj_Apr08.csv: IHME projected death and inferred infection rate
