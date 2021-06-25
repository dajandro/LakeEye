# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 23:46:03 2021

@author: da_or
"""

import pandas as pd
import numpy as np
import math

def is_outlier_modZscore(values, threshold=3.5):
    median_y = np.median(values)
    median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in values])
    if median_absolute_deviation_y==0:
        MAE=np.sum([abs(y-median_y) for y in values])/len(values)
        modified_z_scores = [(y - median_y) / (1.253314*MAE) for y in values]
    else:
        modified_z_scores = [0.6745 * (y - median_y) / median_absolute_deviation_y for y in values]
        
    return (np.abs(modified_z_scores) > threshold)

def get_ranks(dfQ, dfT):
    df = pd.DataFrame(columns=['LAKE_ID', 'DATE', 'TYPE', 'TSI', 'TURBIDITY', 'TEMPERATURE'])
    
    df = get_recent_representative_lwq(dfQ)
    df = get_recent_representative_lswt(dfT, df)
    
    df['RANK 1'] = df.apply(lambda x: rank1(x.TSI), axis=1)
    df['RANK 2'] = df.apply(lambda x: rank2(x.TURBIDITY, x.TEMPERATURE), axis=1)
    
    return df
    

def get_recent_representative_lwq(dfQ):
    # Search for most recent date with values per measurement
    ## Transpose
    dfQ2 = dfQ.melt(['DATE', 'PRODUCT', 'ID', 'NAME', 'Latitude', 'Longitude'], var_name='MEASUREMENT', value_name='VALUE')
    #dfQ2.ID.nunique()
    ## Group and Max
    dfQ3 = dfQ2.groupby('ID', sort=False)['DATE'].max().to_frame()
    
    df = pd.DataFrame(columns=['LAKE_ID', 'DATE', 'TYPE', 'TSI', 'TURBIDITY', 'TEMPERATURE'])

    # Iterate over lakes and dates
    for i, row in dfQ3.iterrows():
        lake = i
        date = row['DATE']
        print(lake+' '+str(date))
        
        # TSI
        tsi = dfQ[(dfQ.ID==lake) & (dfQ.DATE==date)]['trophic_state_index'].values
        tsi_w = 1-dfQ[(dfQ.ID==lake) & (dfQ.DATE==date)]['tsi_risk_ratio'].values
        ## Remove outliers from trophic_state_index
        tsi_o = is_outlier_modZscore(tsi)
        #print((np.count_nonzero(tsi_o)/len(tsi))*100)
        tsi = tsi[~ tsi_o]
        tsi_w = tsi_w[~ tsi_o]
        
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
            
        df_i = pd.DataFrame()
        df_i['LAKE_ID'] = [lake]
        df_i['DATE'] = [date]
        df_i['TYPE'] = ['AVG']
        df_i['TSI'] = [tsi_avg]
        df_i['TURBIDITY'] = [tur_avg]
        df = df.append(df_i)
        
        df_i = pd.DataFrame()
        df_i['LAKE_ID'] = [lake]
        df_i['DATE'] = [date]
        df_i['TYPE'] = ['MEDIAN']
        df_i['TSI'] = [tsi_med]
        df_i['TURBIDITY'] = [tur_med]
        df = df.append(df_i)
        
        df_i = pd.DataFrame()
        df_i['LAKE_ID'] = [lake]
        df_i['DATE'] = [date]
        df_i['TYPE'] = ['WEIGHTED AVG']
        df_i['TSI'] = [tsi_wavg]
        df_i['TURBIDITY'] = [tur_wavg]
        df = df.append(df_i)
        
    df.reset_index(drop=True, inplace=True)
    return df

def get_recent_representative_lswt(dfT, df):
    # Search for most recent date with values per measurement
    dfT2 = dfT.groupby('LAKE_ID', sort=False)['MEASUREMENT_DATE'].max().to_frame()
    # Iterate over lakes and dates
    for i, row in dfT2.iterrows():
        lake = i
        date = row['MEASUREMENT_DATE']
        print(lake+' '+str(date))
        
        # TEMPERATURE
        tem = dfT[(dfT.LAKE_ID==lake) & (dfT.MEASUREMENT_DATE==date)]['TEMP_AVG'].values
        print('\tTEMPERATURE')
        print('\t\t Avg: '+str(tem[0]))
        
        df.loc[df.LAKE_ID==lake, 'TEMPERATURE']=[tem]
    
    return df

def rank1(TSI):
    if (math.isnan(TSI)):
        return math.nan
    if (TSI <= 10):
        return 1
    if (TSI <= 30):
        return 2
    if (TSI <= 50):
        return 3
    if (TSI <= 70):
        return 4
    return 5

def rank2(TUR, TEMP, a=0.5, b=0.5):
    if(math.isnan(TUR) and math.isnan(TEMP)):
        return math.nan
    # TUR rank
    TUR_r = math.nan
    if (not math.isnan(TUR)):
        if (TUR <= 10.0):
            TUR_r = 1
        elif (TUR > 10.0 and TUR <= 30.0):
            TUR_r = 2
        elif (TUR > 30.0 and TUR <= 50.0):
            TUR_r = 3
        elif (TUR > 50.0 and TUR <= 70.0):
            TUR_r = 4
        else:
            TUR_r = 5
    
    # TEMP rank
    TEMP_r = math.nan
    if (not math.isnan(TEMP)):
        if (TEMP >= 20):
            TEMP_r = 1
        elif (TEMP < 20 and TEMP >= 15):
            TEMP_r = 2
        elif (TEMP < 15 and TEMP >= 12):
            TEMP_r = 3
        elif (TEMP < 12 and TEMP >= 10):
            TEMP_r = 4
        else:
            TEMP_r = 5
    
    if (math.isnan(TUR)):
        return TEMP_r
    
    if (math.isnan(TEMP)):
        return TUR_r
    
    return TUR_r*a + TEMP_r*b
