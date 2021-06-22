# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:39:45 2021

@author: da_or
"""

import netCDF4 as nc
import cgls_lib as lib
import re
from datetime import datetime, date
import pandas as pd

# Get lakes
lakes = lib.get_lakes()

# Define products
products = ['cgls_lwq', 'cgls_lswt']

# Define measurements
measurements_lwq = ['trophic_state_index', 'num_obs', 'n_obs_quality_risk_sum', 'stats_valid_obs_tsi_sum', 'turbidity_mean', 'turbidity_sigma', 'stats_valid_obs_turbidity_sum']
measurements_lswt = ['lake_surface_water_temperature']

# Process products for all lakes
for i in range(len(products)):
    df = pd.DataFrame()
    
    p_i = products[i]
    print('Processing '+p_i)
    # Define measurements
    measurements = measurements_lwq if p_i=='cgls_lwq' else (measurements_lswt if p_i=='cgls_lswt' else [])
    
    # Files not yet processed
    files = lib.search_files_to_process(p_i)
    print(str(len(files)) + ' file(s)')
    
    # Iterate files
    for j in range(len(files)):
        f_j = files[j]
        dt_pattern = re.compile('[\d]{4}[\d]{2}[\d]{2}')
        dt_org = dt_pattern.search(f_j).group(0)
        dt = datetime.strptime(dt_org, '%Y%m%d').strftime('%Y-%m-%d')
        print('Processing file from ' + dt)
        
        # Load NC file
        ds = nc.Dataset('../../data/'+f_j)
        
        # Process
        df_i_j = lib.process_lakes(p_i, lakes, ds, measurements)
        df_i_j.insert(loc=0, column='PRODUCT', value=p_i)
        df_i_j.insert(loc=0, column='DATE', value=dt)
        # Concatenate dataframes
        df = df.append(df_i_j)
    
        # Append processed file to log
        lib.append_log(p_i, 'P', f_j)
        
        # Close NC file
        ds.close()
        
    # Save file
    if(len(df)):
        df.reset_index(drop=True, inplace=True)
        df.to_json('../../data/' + p_i + '_' + date.today().strftime('%Y-%m-%d') + '.json')
    
        