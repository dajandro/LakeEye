# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:15:39 2021

@author: da_or
"""
import pandas as pd
import lib as lib
import datetime

# Read TSI and Turbidity
dfQ = pd.read_json('../../data/cgls_lwq_2021-06-22.json', convert_dates=False)
## Set date datatype
dfQ['DATE'] = dfQ['DATE'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date())

# Read Temperature
dfT = pd.read_json('../../data/gdb_lswt_2021-06-22.json', convert_dates=False)
## Set date datatype
dfT['MEASUREMENT_DATE'] = dfT['MEASUREMENT_DATE'].apply(lambda x: datetime.datetime.strptime(x, '%d.%m.%Y').date())

# Assing ranks - Static models
df = lib.get_ranks(dfQ, dfT)