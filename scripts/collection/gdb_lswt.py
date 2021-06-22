# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 16:07:51 2021

@author: da_or
"""

import pandas as pd
from datetime import date

start_dt = '01.04.2021'
end_dt = '22.06.2021'

lake_url = [
    ['DE_BY_001','isar/ammerseeboje-16601050/'],
    ['DE_BY_002','isar/starnberg-16663002/'],
    ['DE_BY_005','inn/buchwinkel-18682507/'],
    ['DE_BY_006','inn/stock-18400503/'],
    ['DE_BY_007','iller_lech/lindau-20001500/'],
    ['DE_BY_009','iller_lech/rottachsee-11444001/'],
    ['DE_BY_010','kelheim/brombachsee-vorsperre-24214445/']
]

df = pd.DataFrame()

# Iterate over lakes
for i in range(len(lake_url)):
    df_i = pd.DataFrame()
    
    # Base URL
    url = 'https://www.gkd.bayern.de/en/lakes/watertemperature/'
    
    l_u_i = lake_url[i]
    l_i = l_u_i[0]
    u_i = l_u_i[1]
    
    # Complete url
    url += u_i + 'total-period/table' + '?beginn='+start_dt+'&ende='+end_dt
  
    # Query and parse table 
    ## Special cases (Table)
    if (l_i=='DE_BY_001'):
        df_i = pd.read_html(url, skiprows=[1])[1]
        # Stay with temperature in water depht of 0,5m
        df_i = df_i.iloc[:, 0:2]
        df_i['TEMP_MAX'] = 0
        df_i['TEMP_MIN'] = 0
    else:
        df_i = pd.read_html(url)[1]
    
    # Rename columns
    df_i.columns = ['MEASUREMENT_DATE', 'TEMP_AVG', 'TEMP_MAX', 'TEMP_MIN']
        
    
    # Add ID
    df_i.insert(loc=0, column='LAKE_ID', value=l_i)
    
    # Validate non empty dataset
    if (len(df_i)):
        df = df.append(df_i)
        
# Write dataframe to file
if (len(df)):
    df.reset_index(drop=True, inplace=True)
    df.to_json('../../data/gdb_lswt_' + date.today().strftime('%Y-%m-%d') + '.json')