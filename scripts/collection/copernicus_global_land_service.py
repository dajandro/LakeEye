# -*- coding: utf-8 -*-
"""
Created on Mon May  3 19:49:51 2021

@author: da_or
"""

import requests
from urllib.parse import urlencode

base_url = 'https://land.copernicus.vgt.vito.be/PDF/RDA'
params = {
    'fwu' : 'https://globalland.cls.fr/webResources/nc/brockmann/LWQ-NRT-300m/dataset/c_gls_LWQ300_202104110000_GLOBE_OLCI_V1.4.0.nc'
    ,'ps' : 0
    ,'collectionID' : '1100501'
    ,'productID' : 'c_gls_LWQ300_202104110000_GLOBE_OLCI_V1.4.0'
    ,'coord' : '-179.998883929,-89.9988839286,179.998883929,89.9988839286'
}

params_lswt = {
    'fwu' : 'https://globalland.cls.fr/webResources/nc/brockmann/LSWT-NRT/dataset/c_gls_LSWT_202104110000_GLOBE_SLSTRAB_v1.1.0.nc'
    ,'ps' : 0
    ,'collectionID' : '1100101'
    ,'productID' : 'LSWT_202104110000_GLOBE_SLSTRAB_V1.1.0.4.0'
    ,'coord' : '-179.998883929,-89.9988839286,179.998883929,89.9988839286'
}

#qstr = urlencode(params_lswt)
qstr = urlencode(params)

url = base_url + '?' + qstr
print("Fetching from: "+url)
r = requests.get(url, auth=('usr', 'pass'), stream=True)
print("\nStatus code: "+str(r.status_code))
#print(r.headers)
f_name = (r.headers['Content-disposition']).split('filename=')[1]
print("\nFile: "+f_name)
#print(r.cookies)

f = open('test_'+f_name, 'wb')
for chunk in r.iter_content(chunk_size=1024):
    f.write(chunk)
    #print("chunk writed")
    
f.close()

