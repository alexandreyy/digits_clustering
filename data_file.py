'''
Created on 20/04/2015

@author: Alexandre Yukio Yamashita
'''
import os

import numpy as np


def read_file (file_path):
    '''
    Read data file, if it exists.
    '''
    # Check if file exists,
    if os.path.isfile(file_path):
        # Read data file,
        print "Reading data file."
        
        data_file = open(file_path, "r")
        data_read = np.float32(np.loadtxt(data_file, delimiter=','))       
        data_file.close()
        
        return data_read
    else:
        # File not found.
        print "File doesn't exist."
        return None
