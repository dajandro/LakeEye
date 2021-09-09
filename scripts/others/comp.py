# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 14:28:33 2021

@author: da_or
"""

import netCDF4 as nc
import cgls_lib as lib
import pandas as pd

measurements_lwq = ['trophic_state_index', 'num_obs', 'n_obs_quality_risk_sum', 'stats_valid_obs_tsi_sum', 'turbidity_mean', 'turbidity_sigma', 'stats_valid_obs_turbidity_sum']
measurements_lswt = ['lake_surface_water_temperature']

lakes = lib.get_lakes()
test_lake = 'Starnberger See'

ds_q = nc.Dataset('../../data/_c_gls_LWQ300_202104210000_GLOBE_OLCI_V1.4.0.nc')
df_q = lib.process_lake('', lakes[lakes.NAME==test_lake], ds_q, measurements_lwq)
df_p_q = pd.read_json('../../data/cgls_lwq_2021-06-22.json')

ds_t = nc.Dataset('../../data/c_gls_LSWT_202104210000_GLOBE_SLSTRAB_v1.1.0.nc')
df_p_t = pd.read_json('../../data/cgls_lswt_2021-06-22.json')

t_df_p_q = df_p_q[df_p_q.NAME == test_lake]

lib.plt_stats(t_df_p_q, 'trophic_state_index')
lib.plt_stats(df_q, 'trophic_state_index')