# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 09:33:00 2020

@author: petko
"""

from datetime import datetime,timedelta
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # plot functionality
import sys
import os

# Importing IHME Data (downloaded from http://www.healthdata.org/covid/data-downloads) and converted to only contain US state data
dirname=sys.path[0]
files = [f for f in os.listdir('./') if os.path.isfile(f) and f.endswith('csv')]
for filename in files:
    if "IHME_USA_Proj_Apr08.csv"==filename:
        print(os.path.join(dirname, filename))
        pathname=os.path.join(dirname, filename)
        df_proj=pd.read_csv(filename,parse_dates=['date'],infer_datetime_format=True)

df_grouped=df_proj.groupby('date').agg(['sum'])
df_daily=df_grouped.reset_index()

# US Day by Day Projected Infections IMHE
fig, ax = plt.subplots()
plt.title('Projected US New Daily Infections (IHME)')
plt.plot(df_daily.date, df_daily.projected_infections,'r--',)
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.xticks(rotation=45)
plt.show()

# Creating 5 Day Treatment Window and use 400mg per day
df_proj['5day_infected_HQregimen_patients']=df_proj.projected_infections.rolling(5,min_periods=1).agg(['sum'])
dfAggByDate=df_proj.groupby("date")['5day_infected_HQregimen_patients'].agg('sum')
dfAggByDate[dfAggByDate<0]=0
dfwithHQPills=pd.DataFrame({'cases':dfAggByDate,'HQ_Pills':dfAggByDate.values*2})

# Assuming 5-day treatment plan how many patients would be subject to a HCQ regimen if prescribed to all patients
fig2, ax2 = plt.subplots()
plt.xticks(rotation=45)
plt.title('Rolling 5 Day Window of US Patients')
ax2.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.plot(dfAggByDate.index, dfwithHQPills.cases,'r--')

# Hydroxychloroquine Daily Usage if prescribed to all patients and assuming medium level projected IMHE infection curve
fig3, ax3 = plt.subplots()
plt.title('HCQ US Daily Pill Projected Need')
plt.xticks(rotation=45)
ax3.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.plot(dfAggByDate.index, dfwithHQPills.HQ_Pills,'r--')

# Total Number of Pills Needed
cumulative_pills=dfwithHQPills.HQ_Pills.cumsum().tail(120)
fig4, ax4 = plt.subplots()
plt.title('HCQ US Cumulative Pill Projected Need')
plt.xticks(rotation=45)
ax4.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
plt.plot(dfAggByDate.tail(120).index, cumulative_pills.values,'r--')

# Cumulative Pills Needed and $ Cost
total_pills=dfwithHQPills.HQ_Pills.cumsum().tail(1)
# Cost Calc. *ignoring donations* and assume 4x developing world cost
total_price=.04*4*total_pills
