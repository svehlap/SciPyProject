import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import listdir
from os.path import isfile, isdir, join

data = pd.DataFrame()

#mypath = os.getcwd()

groups = [f for f in listdir(mypath)]
for group in groups:
    
    # extraxt folder names
    subfolders = [f for f in listdir(join(mypath, group))]
    # check if further subfolders exist
    for subfolder in subfolders:
    #    if ~isdir(join(mypath, subfolder)):
        files = [f for f in listdir(join(mypath, group, subfolder))]
        for file in files:
            data_tmp = pd.read_csv(join(mypath, group, subfolder, file))
                
            ls = [1]
            ls[0] = group
            ls = ls*len(data_tmp)
            data_tmp['ExpGroup'] = ls
            
            ls = [1]
            ls[0] = subfolder
            ls = ls*len(data_tmp)
            data_tmp['MouseID'] = ls
            
            ls = [1]
            ls[0] = file
            ls = ls*len(data_tmp)
            data_tmp['FileID'] = ls
            
            
            data = data.append(data_tmp)


            
        
#for root, dirs, files in os.walk(path):
#   for name in files:
