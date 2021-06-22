# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 16:07:51 2021

@author: da_or
"""

import pandas as pd

start_dt = '01.05.2021'
end_dt = '22.06.2021'

url = 'https://www.gkd.bayern.de/en/lakes/watertemperature/'

# Bodensee path
#url += 'iller_lech/lindau-20001500/current-values/table'
# Chiemsee path
#url += 'inn/stock-18400503/current-values/table'
# Waginger See
#url += '/inn/buchwinkel-18682507/current-values/table'
# Starnberger See
url += 'isar/starnberg-16663002/current-values/table'
# Amersee path
#url += 'isar/ammerseeboje-16601050/current-values/table'

# Append date
url += '?beginn='+start_dt+'&ende='+end_dt

df = pd.read_html(url)[1]