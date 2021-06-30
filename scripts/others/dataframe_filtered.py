# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:15:08 2021

@author: Delma
"""


import numpy as np
import pandas as pd

df_filtered=pd.DataFrame()


def outliers_modified_z_score(ys):
    tsif=ys['trophic_state_index']
    threshold = 3.5
    median_tsi = np.median(tsif)
    median_absolute_deviation_tsi = np.median([np.abs(tsi - median_tsi) for tsi in tsif])
    if median_absolute_deviation_tsi==0:
        MAE=np.sum([abs(tsi-median_tsi) for tsi in tsif])/len(tsif)
        modified_z_scores = [(tsi - median_tsi) / (1.253314*MAE) for tsi in tsif]
    else:
        modified_z_scores = [0.6745 * (tsi - median_tsi) / median_absolute_deviation_tsi for tsi in tsif]
    ys=ys[~(np.abs(modified_z_scores) > threshold)]
    return ys



df=pd.read_json (r'cgls_lwq_2021-06-09.json')
lakes = ['Amersee','Starnberger See','Walchensee','Chiemsee','Bodensee','Forggensee']

for lake in lakes:
    lakefile=df[df.NAME==lake]
    lakefile_filtered=outliers_modified_z_score(lakefile)
    df_filtered=pd.concat([df_filtered, lakefile_filtered], axis=0)
    
#large_df = pd.concat(small_dfs, ignore_index=True)
    


