# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 16:07:51 2021

@author: da_or
"""

import pandas as pd

start_dt = '01.05.2021'
end_dt = '22.06.2021'

url = 'https://www.gkd.bayern.de/en/lakes/watertemperature/inn/stock-18400503/current-values/table'
url += '?beginn='+start_dt+'&ende='+end_dt

df = pd.read_html(url)[1]