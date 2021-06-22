# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:15:39 2021

@author: da_or
"""
import pandas as pd

# Read TSI and Turbidity
dfQ = pd.read_json('../../data/cgls_lwq_2021-06-22.json')

# Read Temperature
dfT = pd.read_json('../../data/gdb_lswt_2021-06-22.json')

# Remove outliers

# Static models

## Mean
## Median
## Weighted average