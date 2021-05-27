# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:39:45 2021

@author: da_or
"""

import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

# Filter latitudes inside defined range
lt = np.array(lats)
## Get index
lt_index = np.argwhere((lt>=min_lat) & (lt<=max_lat))[:,0]

# Filter longitudes inside defined range
lg = np.array(lons)
## Get index
lg_index = np.argwhere((lg>=min_lon) & (lg<=max_lon))[:,0]

# Filter measurement by lat & lon index
measurement = 'turbidity_mean'
t = ds[measurement][0,lt_index[0]:lt_index[len(lt_index)-1],lg_index[0]:lg_index[len(lg_index)-1]]
## Get index of cells without mask (non empty or valid)
t_v = np.argwhere(t.mask==False)
if (not len(t_v)):
    print('No data available for the specified region')
else:    
    # Valid latitudes
    lt_valid = lt[lt_index[t_v[:,0]]]
    # Valid longitudes
    lg_valid = lg[lg_index[t_v[:,1]]]
    # Valid measurements
    m_valid = t.data[t_v[:,0],t_v[:,1]]
    
    # Create dataframe
    df = pd.DataFrame(list(zip(lt_valid, lg_valid, m_valid)), columns=['Latitude', 'Longitude', measurement])
    
    # Statistics plot
    fig, ax = plt.subplots()
    ax.hist(m_valid)
    plt.figtext(0.75,0.7, df[measurement].describe().to_string())
    plt.figtext(0.75,0.3, df[measurement].describe().loc[['mean','std']].to_string())
    plt.show()
    
    # Measurements plot
    sc = plt.scatter(lg_valid, lt_valid, c=m_valid, cmap=plt.cm.get_cmap('winter'))
    plt.colorbar(sc)
    plt.gca().set_aspect('equal')
    plt.show()