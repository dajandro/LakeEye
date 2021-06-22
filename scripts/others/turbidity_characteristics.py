# -*- coding: utf-8 -*-
"""
Mean, Median, Weighted average for the turbidity for each lake.
Data used is from json files.

@author: francgr
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_json (r'cgls_lwq_2021-06-09.json')
df['tur_risk_ratio'] = df['n_obs_quality_risk_sum'] / df['stats_valid_obs_turbidity_sum']

lake_names = ['Amersee','Starnberger See','Walchensee','Chiemsee','Bodensee','Forggensee']


for i in lake_names:
    mean = np.mean(df[df.NAME== i]['turbidity_mean'])
    median = np.median(df[df.NAME== i]['turbidity_mean'])
    w = (1-df[df.NAME== i]['tur_risk_ratio'])
    x = df[df.NAME== i]['turbidity_mean']
    weighted_average = np.sum( w*x )/(np.sum(w))
    print('Turbidity Mean for ', i , 'is ', mean)
    print('Turbidity Median for ', i , 'is ', median)
    print('Turbidity W average for ', i , 'is ', weighted_average)
    
    