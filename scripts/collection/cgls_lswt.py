# -*- coding: utf-8 -*-
"""
Created on Wed May  5 15:03:14 2021

@author: da_or
"""
# Copernicus Global Land Service - Lake Surface Water Temperature

import cgls_lib as lib

# FTP server
url = 'ftp.globalland.cls.fr'
# Product path
product_path = 'Core/BROCKMANN/dataset-brockmann-lswt-nrt/'
# Product id
product_id = 'cgls_lswt'

lib.fetch_file_ftp(url, 'usr', 'pwd', product_path, product_id)