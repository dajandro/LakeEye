# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 02:17:44 2021

@author: da_or
"""

import pandas as pd
import datetime
import lib as lib
from datetime import date
import math

# Read TSI and Turbidity
dfQ = pd.read_json('../../data/cgls_lwq_2021-06-22.json', convert_dates=False)
## Set date datatype
dfQ['DATE'] = dfQ['DATE'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

# Read Temperature
dfT = pd.read_json('../../data/gdb_lswt_2021-06-22.json', convert_dates=False)
## Set date datatype
dfT['MEASUREMENT_DATE'] = dfT['MEASUREMENT_DATE'].apply(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y').date())

# DB transform
dfQ1 = dfQ[['ID', 'Latitude', 'Longitude', 'DATE', 'trophic_state_index']]
dfQ1 = dfQ1.melt(['ID', 'Latitude', 'Longitude', 'DATE'], var_name='MEASUREMENT', value_name='VALUE')
dfQ1['MEASUREMENT'] = 1

dfQ2 = dfQ[['ID', 'Latitude', 'Longitude', 'DATE', 'turbidity_mean']]
dfQ2 = dfQ2.melt(['ID', 'Latitude', 'Longitude', 'DATE'], var_name='MEASUREMENT', value_name='VALUE')
dfQ2['MEASUREMENT'] = 2

dfQf = dfQ1.append(dfQ2)
## Write file
#dfQf.to_csv('lwq.txt', index=False)

dfTf = pd.DataFrame(columns=['LAKE_ID', 'LAT', 'LON', 'MEASUREMENT_ID', 'VAL_QTY', 'MEASUREMENT_DT'])
dfTf['LAKE_ID'] = dfT['LAKE_ID']
dfTf['LAT'] = ''
dfTf['LON'] = ''
dfTf['MEASUREMENT_ID'] = 4
dfTf['VAL_QTY'] = dfT['TEMP_AVG']
dfTf['MEASUREMENT_DT'] = dfT['MEASUREMENT_DATE']
## Write file
#dfTf.to_csv('lswt.txt', index=False)

df = lib.get_ranks(dfQ, dfT)
model = "WEIGHTED AVG"
dff = df[df.TYPE==model]
dff1 = pd.DataFrame(columns=['LAKE_ID', 'PARAMETER_ID', 'VAL_NUM', 'MODEL', 'MODIFICATION_DT'])
dff1['LAKE_ID'] = dff['LAKE_ID']
dff1['PARAMETER_ID'] = 1
dff1['VAL_NUM'] = dff['TSI']
dff1['MODEL'] = model
dff1['MODIFICATION_DT'] = date.today().strftime('%Y-%m-%d')
dff2 = pd.DataFrame(columns=['LAKE_ID', 'PARAMETER_ID', 'VAL_NUM', 'MODEL', 'MODIFICATION_DT'])
dff2['LAKE_ID'] = dff['LAKE_ID']
dff2['PARAMETER_ID'] = 2
dff2['VAL_NUM'] = dff['TURBIDITY']
dff2['MODEL'] = model
dff2['MODIFICATION_DT'] = date.today().strftime('%Y-%m-%d')
dfff = dff1.append(dff2)
dff3 = pd.DataFrame(columns=['LAKE_ID', 'PARAMETER_ID', 'VAL_NUM', 'MODEL', 'MODIFICATION_DT'])
dff3['LAKE_ID'] = dff['LAKE_ID']
dff3['PARAMETER_ID'] = 3
dff3['VAL_NUM'] = dff['TEMPERATURE']
dff3['MODEL'] = model
dff3['MODIFICATION_DT'] = date.today().strftime('%Y-%m-%d')
dfff = dfff.append(dff3)
dfff = dfff.replace(math.nan, '', regex=True)
## Write file
#dfff.to_csv('params.txt', index=False)

dfR1 = pd.DataFrame(columns=['LAKE_ID', 'RANK_ID', 'VAL_NUM', 'MODIFICATION_DT'])
dfR1['LAKE_ID'] = dff['LAKE_ID']
dfR1['RANK_ID'] = 1
dfR1['VAL_NUM'] = dff['RANK 1']
dfR1['MODIFICATION_DT'] = date.today().strftime('%Y-%m-%d')
dfR2 = pd.DataFrame(columns=['LAKE_ID', 'RANK_ID', 'VAL_NUM', 'MODIFICATION_DT'])
dfR2['LAKE_ID'] = dff['LAKE_ID']
dfR2['RANK_ID'] = 2
dfR2['VAL_NUM'] = dff['RANK 2']
dfR2['MODIFICATION_DT'] = date.today().strftime('%Y-%m-%d')
dfRf = dfR1.append(dfR2)
## Write file
#dfRf.to_csv('ranks.txt', index=False)