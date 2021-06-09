# -*- coding: utf-8 -*-
"""
Created on Thu May 27 17:54:11 2021

@author: da_or
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

def read_log(product, log_type, path='../../logs/'):
    file = open(path + product + '-' + log_type + '.log', 'r')
    entries = file.readlines()
    file.close()
    return entries

def append_log(product, log_type, data, path='../../logs/'):
    file = open(path + product + '-' + log_type + '.log', 'a')
    file.write(f'\n{data}')
    file.close()
    
def get_lakes(path='../../db/lakes.json'):
    file = open(path, 'r')
    with open(path) as file:
        data = json.loads(file.read())
        
    return(pd.json_normalize(data, record_path=['lakes']))
    
def search_files_to_process(product):
    d = read_log(product, 'D')
    p = read_log(product, 'P')
    return (list(set(p).symmetric_difference(set(d))))

def plt_scatter(df, measurement):
    sc = plt.scatter(df['Longitude'], df['Latitude'], c=df[measurement], cmap=plt.cm.get_cmap('winter'))
    plt.colorbar(sc)
    plt.gca().set_aspect('equal')
    plt.show()
    
def plt_stats(df, measurement):
    fig, ax = plt.subplots()
    ax.hist(df[measurement])
    plt.figtext(0.75,0.7, df[measurement].describe().to_string())
    plt.figtext(0.75,0.3, df[measurement].describe().loc[['mean','std']].to_string())
    plt.show()

def get_measurement(ds, m_name, lt, lg, lt_rgn_index, lg_rgn_index):
    # Filter measurement by lat & lon index
    t = ds[m_name][0,lt_rgn_index[0]:lt_rgn_index[len(lt_rgn_index)-1],lg_rgn_index[0]:lg_rgn_index[len(lg_rgn_index)-1]]
    # Get index of cells without mask (non empty or valid)
    t_v = np.argwhere(t.mask==False)
    
    # Validate empty measurements
    if (not len(t_v)):
        print('No data available for the specified region')
        return pd.DataFrame()
   
    # Valid latitudes
    lt_valid = lt[lt_rgn_index[t_v[:,0]]]
    # Valid longitudes
    lg_valid = lg[lg_rgn_index[t_v[:,1]]]
    # Valid measurements
    m_valid = t.data[t_v[:,0],t_v[:,1]]
    
    # Create dataframe
    df = pd.DataFrame(list(zip(lt_valid, lg_valid, m_valid)), columns=['Latitude', 'Longitude', m_name])
    return df
    
def get_measurements(ds, m_names, lt, lg, lt_rgn_index, lg_rgn_index):
    if(not len(m_names)):
        return pd.DataFrame()
    # Initialize with first measurement
    df = get_measurement(ds, m_names[0], lt, lg, lt_rgn_index, lg_rgn_index)
    # Iterate measurements
    for i in range(1,len(m_names)):
        m_i = m_names[i]
        df_m_i = get_measurement(ds, m_i, lt, lg, lt_rgn_index, lg_rgn_index)
        if (not len(df_m_i)):
            continue
        # Merge with latitude and longitude
        df = df.merge(df_m_i, how='inner', left_on=['Latitude', 'Longitude'], right_on=['Latitude', 'Longitude'])
    return df
        
def process_lakes(product, lakes, ds, measurements):
    df = pd.DataFrame()
    for i in range(len(lakes)):
        lake_i = lakes.iloc[[i]]
        ID = lake_i.GLS_ID.values[0]
        name = lake_i.NAME.values[0]
        print('\t'+name)
        df_lake_i = process_lake(product, lake_i, ds, measurements)
        df_lake_i.insert(loc=0, column='NAME', value=name)
        df_lake_i.insert(loc=0, column='ID', value=ID)
        # Concatenate dataframes
        df = df.append(df_lake_i)
        
    return df

def process_lake(product, lake, ds, measurements):
    # Define grid
    lats = ds['lat'][:]
    lons = ds['lon'][:]
    
    # Filter latitudes inside defined range
    lt = np.array(lats)
    ## Get index
    min_lat = lake.MN_LAT.values[0]
    max_lat = lake.MX_LAT.values[0]
    lt_index = np.argwhere((lt>=min_lat) & (lt<=max_lat))[:,0]
    
    # Filter longitudes inside defined range
    lg = np.array(lons)
    ## Get index
    min_lon = lake.MN_LON.values[0]
    max_lon = lake.MX_LON.values[0]
    lg_index = np.argwhere((lg>=min_lon) & (lg<=max_lon))[:,0]
    
    # Extract measurements of desired variables in specific region
    df = get_measurements(ds, measurements, lt, lg, lt_index, lg_index)
    
    if (not len(df)):
        return df
    
    # Special pre-process for each product
    if(product=='cgls_lwq'):
        # Add clorophyll-a (upper limit)
        df['clorophyll-a'] = np.exp(((-((df['trophic_state_index']/10)-6)*np.log(2))-2.04)/-0.68)
        
        # Filter TSI with # of risky observations and # of observations used
        ## risk_ratio = # risk obs / # obs used
        df['tsi_risk_ratio'] = df['n_obs_quality_risk_sum'] / df['stats_valid_obs_tsi_sum']
        df2 = df.query('tsi_risk_ratio<0.5')
        print(str(len(df)-len(df2))+" observations don't fulfill the TSI risk ratio")
        return df2
    
    if(product=='cgls_lswt'):
        return df
    
    return df