import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import listdir
from os.path import isfile, isdir, join
import scipy.stats as stats

data = pd.DataFrame()

mypath = join(os.path.dirname(__file__), 'data')

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


data.groupby('ExpGroup').describe()

# total spine density
ctrl_ids = data.loc[:,'ExpGroup'] == 'CTRL'
auto_ids = data.loc[:,'AUTO'] == 'yes'

len(data.loc[:,'SECTION-LENGTH'][ctrl_ids]) / sum(data.loc[:,'SECTION-LENGTH'][ctrl_ids & auto_ids])
  

# spine morphology
# how many neck diameters is nan
len(data.loc[:,'NECK-DIAMETER'][np.isnan(data.loc[:,'NECK-DIAMETER']) == True]) / len(np.isnan(data.loc[:,'NECK-DIAMETER']))

f, axs = plt.subplots(1,3)
nbins = 15
labels = ('CTRL','NMDAR')

# for currExpGroup in  groups:
#     for ind, val in enumerate(['HEAD-DIAMETER', 'NECK-DIAMETER', 'MAX-DTS']):
#             StuffToPlot = np.array(data.loc[:,val][data.loc[:,'ExpGroup'] == currExpGroup])
#             x = np.arange(StuffToPlot.min(), StuffToPlot.max(), 0.1)
#             y = StuffToPlot.cdf(x)
#             axs[ind].plot(x,y, '-')
        
 
StuffToPlot = [data.loc[:,'HEAD-DIAMETER'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'HEAD-DIAMETER'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[0].hist(StuffToPlot, bins=nbins, density=True, cumulative=True)    
axs[0].set_title('Head diameter')     
StuffToPlot = [data.loc[:,'NECK-DIAMETER'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'NECK-DIAMETER'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[1].hist(StuffToPlot, bins=nbins, density=True, cumulative=True)  
axs[1].set_title('Neck diameter')            
StuffToPlot = [data.loc[:,'MAX-DTS'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'MAX-DTS'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[2].hist(StuffToPlot, label=labels, bins=nbins, density=True, cumulative=True)   
axs[2].set_title('Spine length')           
f.legend()


#for root, dirs, files in os.walk(path):
#   for name in files:
