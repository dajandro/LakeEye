# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 23:46:03 2021

@author: da_or
"""

import numpy as np

def outliers_modified_z_score(values):
    threshold = 3.5
    median_y = np.median(values)
    median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in values])
    if median_absolute_deviation_y==0:
        MAE=np.sum([abs(y-median_y) for y in values])/len(values)
        modified_z_scores = [(y - median_y) / (1.253314*MAE) for y in values]
    else:
        modified_z_scores = [0.6745 * (y - median_y) / median_absolute_deviation_y for y in values]
    
    return np.asarray(np.where(np.abs(modified_z_scores) > threshold))[0]