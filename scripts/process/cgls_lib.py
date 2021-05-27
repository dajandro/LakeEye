# -*- coding: utf-8 -*-
"""
Created on Thu May 27 17:54:11 2021

@author: da_or
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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
        return
   
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
        return
    # Initialize with first measurement
    df = get_measurement(ds, m_names[0], lt, lg, lt_rgn_index, lg_rgn_index)
    # Iterate measurements
    for i in range(1,len(m_names)):
        m_i = m_names[i]
        df_m_i = get_measurement(ds, m_i, lt, lg, lt_rgn_index, lg_rgn_index)
        if (not len(df)):
            continue
        # Merge with latitude and longitude
        df = df.merge(df_m_i, how='inner', left_on=['Latitude', 'Longitude'], right_on=['Latitude', 'Longitude'])
    return df
        
        