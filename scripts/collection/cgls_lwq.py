# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:56:38 2021

@author: da_or
"""
# Copernicus Global Land Service - Lake Water Quality

import cgls_lib as lib

# FTP server
url = 'ftp.globalland.cls.fr'
# Product path
product_path = 'Core/BROCKMANN/dataset-brockmann-lwq-nrt-300m/'
# Product id
product_id = 'cgls_lwq'

lib.fetch_file_ftp(url, 'usr', 'pwd', product_path, product_id)