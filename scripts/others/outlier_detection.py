# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 21:55:02 2021

@author: Delma
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def outliers_z_score(ys): 
    threshold=3 # 3 times the standard deviation
    z_mu=np.mean(ys)
    z_sig=np.std(ys)
    z_scores = [(y - z_mu) / z_sig for y in ys]
    return np.where(np.abs(z_scores) > threshold)

def outliers_modified_z_score(ys):
    threshold = 3.5
    median_y = np.median(ys)
    median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in ys])
    if median_absolute_deviation_y==0:
        MAE=np.sum([abs(y-median_y) for y in ys])/len(ys)
        modified_z_scores = [(y - median_y) / (1.253314*MAE) for y in ys]
    else:
        modified_z_scores = [0.6745 * (y - median_y) / median_absolute_deviation_y for y in ys]
    
    return np.where(np.abs(modified_z_scores) > threshold)

def outliers_iqr(ys):
    quartile_1, quartile_3 = np.percentile(ys, [25, 75])
    iqr = quartile_3 - quartile_1
    lower_bound = quartile_1 - (iqr * 1.5)
    upper_bound = quartile_3 + (iqr * 1.5)
    return np.where((ys > upper_bound) | (ys < lower_bound))


df=pd.read_json (r'cgls_lwq_2021-06-09.json')

lakes=['Amersee','Starnberger See','Walchensee','Chiemsee','Bodensee','Forggensee']
for lake in lakes:
    lakename=df[df.NAME==lake];
    lake_TSI=lakename['trophic_state_index'];
    mean_outliers=np.array(outliers_z_score(lake_TSI))
    median_outliers=np.array(outliers_modified_z_score(lake_TSI))
    iqr_outliers=np.array(outliers_iqr(lake_TSI))


    f, (ax1,ax2,ax3) = plt.subplots(1,3)
    ax1.hist(lake_TSI)
    ax1.set_title('Mean Outliers for %s' %(lake))
    for i in mean_outliers:
        ax1.vlines(x=lake_TSI[i],ymin=0,ymax=200, color='r', linewidth=2)
        ax2.hist(lake_TSI)
        ax2.set_title('Median Outliers for %s' %(lake))
    for i in median_outliers:
        ax2.vlines(x=lake_TSI[i],ymin=0,ymax=200, color='r', linewidth=2)
    ax3.hist(lake_TSI)
    ax3.set_title('Interquartile Outliers %s' %(lake))
    for i in iqr_outliers:
        ax3.vlines(x=lake_TSI[i],ymin=0,ymax=200, color='r', linewidth=2)

