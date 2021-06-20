# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:25:28 2021

@author: da_or
"""

import ftplib
import shutil
import urllib.request as request
from contextlib import closing
from datetime import datetime

def read_log(product, path='../../logs/'):
    file = open(path + product + '-D.log', 'r')
    entries = file.readlines()
    file.close()
    return entries

def append_log(product, data, path='../../logs/'):
    file = open(path + product + '-D.log', 'a')
    file.write(f'\n{data}')
    file.close()

def fetch_file_ftp(server, usr, pwd, path, product):
    # Create FTP object
    ftp = ftplib.FTP()
    try:
        # Set connection point
        print('Connecting to ftp server...')
        ftp.connect(server)
        # Authenticate
        ftp.login(usr, pwd)
        
        # Move to directory
        ftp.cwd(path)  
            
        # Find most recent file in directory
        file_name = sorted(ftp.nlst(), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-1]
        file_size = ftp.size(file_name) / (1024 * 1024) #MB
        
        print('\nMost recent file: ' + file_name + ', size: %.2f' % file_size + "MB")
            
        # Validate in product log file
        files = read_log(product)
        if (not file_name in files):            
            # Download file
            print('\nFile download - Start @ ' + datetime.today().strftime("%d/%m/%Y %H:%M:%S"))
            with closing(request.urlopen('ftp://'+usr+':'+pwd+'@'+server+'/'+path+file_name)) as r:
                with open('../../data/' + file_name, 'wb') as f:
                    shutil.copyfileobj(r, f)
            print('\nFile download - End @ ' + datetime.today().strftime("%d/%m/%Y %H:%M:%S"))
            
            # Update product log file
            append_log(product, file_name)
        else:
            print('\nData up to date')
        
    except ftplib.all_errors as e:
        print(e)
        return