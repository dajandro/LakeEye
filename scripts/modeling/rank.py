# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:15:39 2021

@author: da_or
"""
import pandas as pd
import lib as lib
import numpy as np
import datetime

# Read TSI and Turbidity
dfQ = pd.read_json('../../data/cgls_lwq_2021-06-22.json', convert_dates=False)
## Set date datatype
dfQ['DATE'] = dfQ['DATE'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

# Read Temperature
dfT = pd.read_json('../../data/gdb_lswt_2021-06-22.json', convert_dates=False)
## Set date datatype
dfT['MEASUREMENT_DATE'] = dfT['MEASUREMENT_DATE'].apply(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y').date())

# Search for most recent date with values per measurement
## Transpose
dfQ2 = dfQ.melt(['DATE', 'PRODUCT', 'ID', 'NAME', 'Latitude', 'Longitude'], var_name='MEASUREMENT', value_name='VALUE')
#dfQ2.ID.nunique()
## Group and Max
#dfQ3 = dfQ2.groupby(['ID', 'MEASUREMENT'], sort=False)['DATE'].max().to_frame()
dfQ3 = dfQ2.groupby('ID', sort=False)['DATE'].max().to_frame()

dfT2 = dfT.groupby('LAKE_ID', sort=False)['MEASUREMENT_DATE'].max().to_frame()

# Iterate over lakes and dates
for i, row in dfQ3.iterrows():
    lake = i
    date = row['DATE']
    print(lake+' '+str(date))
    
    # TSI
    tsi = dfQ[(dfQ.ID==lake) & (dfQ.DATE==date)]['trophic_state_index'].values
    tsi_w = 1-dfQ[(dfQ.ID==lake) & (dfQ.DATE==date)]['tsi_risk_ratio'].values
    ## Remove outliers from trophic_state_index
    tsi2 = lib.outliers_modified_z_score(tsi)    
    #print(len(tsi))
    #print(len(tsi2))
    #print(len(tsi)-len(tsi2))
    tsi_avg = np.mean(tsi)
    tsi_med = np.median(tsi)
    tsi_wavg = np.sum(tsi_w*tsi)/np.sum(tsi_w)
    print('\tTSI')
    print('\t\t Avg: '+str(tsi_avg))
    print('\t\t Median: '+str(tsi_med))
    print('\t\t Weighted Avg: '+str(tsi_wavg))
    
    # TURBIDITY
    tur = dfQ[(dfQ.ID==lake) & (dfQ.DATE==date)]['turbidity_mean'].values
    tur_w = 1-dfQ[(dfQ.ID==lake) & (dfQ.DATE==date)]['tur_risk_ratio'].values
    tur_avg = np.mean(tur)
    tur_med = np.median(tur)
    tur_wavg = np.sum(tur_w*tur)/np.sum(tur_w)
    print('\tTURBIDITY')
    print('\t\t Avg: '+str(tur_avg))
    print('\t\t Median: '+str(tur_med))
    print('\t\t Weighted Avg: '+str(tur_wavg))
    
print()    

# Iterate over lakes and dates
for i, row in dfT2.iterrows():
    lake = i
    date = row['MEASUREMENT_DATE']
    print(lake+' '+str(date))
    
    # TEMPERATURE
    tem = dfT[(dfT.LAKE_ID==lake) & (dfT.MEASUREMENT_DATE==date)]['TEMP_AVG'].values
    print('\tTEMPERATURE')
    print('\t\t Avg: '+str(tem[0]))

# Remove outliers


# Static models

## Mean
## Median
## Weighted average