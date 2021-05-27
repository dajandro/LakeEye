# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:39:45 2021

@author: da_or
"""

import netCDF4 as nc
import numpy as np
import cgls_lib as lib

# List files not yet processed

# Iterate files

# Read file
file = 'ftp_test_c_gls_LWQ300_202104210000_GLOBE_OLCI_V1.4.0.nc'
ds = nc.Dataset(file)
lats = ds['lat'][:]
lons = ds['lon'][:]
ts = ds['time'][:]

# Chiemsee
min_lat = 47.81
max_lat = 47.94
min_lon = 12.31
max_lon = 12.55

# Amersee
'''min_lat = 47.933
max_lat = 48.077
min_lon = 11.093
max_lon = 11.176'''

# Starnberger See
'''min_lat = 47.818
max_lat = 47.999
min_lon = 11.262
max_lon = 11.364'''

# Filter latitudes inside defined range
lt = np.array(lats)
## Get index
lt_index = np.argwhere((lt>=min_lat) & (lt<=max_lat))[:,0]

# Filter longitudes inside defined range
lg = np.array(lons)
## Get index
lg_index = np.argwhere((lg>=min_lon) & (lg<=max_lon))[:,0]

# List of desired variables
measurements = ['trophic_state_index', 'num_obs', 'n_obs_quality_risk_sum', 'stats_valid_obs_tsi_sum']

# Extract measurements of desired variables in specific region
df = lib.get_measurements(ds, measurements, lt, lg, lt_index, lg_index)

# Add clorophyll-a (upper limit)
df['clorophyll-a'] = np.exp(((-((df['trophic_state_index']/10)-6)*np.log(2))-2.04)/-0.68)

# Filter TSI with # of risky observations and # of observations used
## risk_ratio = # risk obs / # obs used
df['tsi_risk_ratio'] = df['n_obs_quality_risk_sum'] / df['stats_valid_obs_tsi_sum']
df2 = df.query('tsi_risk_ratio<0.5')
print(str(len(df)-len(df2))+" observations don't fulfill the TSI risk ratio")

# Make plots
## Histogram with statistics
lib.plt_stats(df, 'trophic_state_index')
## Scatter (map)
lib.plt_scatter(df, 'trophic_state_index')