import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import listdir
from os.path import isfile, isdir, join
import scipy.stats as stats
from sklearn.decomposition import PCA
from sklearn import cluster

data = pd.DataFrame()

mypath = join(os.path.dirname(__file__), 'data')

groups = [f for f in listdir(mypath)]
for group in groups:
    
    # extraxt folder names
    subfolders = [f for f in listdir(join(mypath, group))]
    # extract subfolder names
    for subfolder in subfolders:
        files = [f for f in listdir(join(mypath, group, subfolder))]
        for file in files: # extract files from subfolders
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

# print some output
print('total of %i spines were counted in %i images' %(len(data), len(data.groupby('FileID'))))

# total spine density
ctrl_ids = data.loc[:,'ExpGroup'] == 'CTRL'
auto_ids = data.loc[:,'AUTO'] == 'yes'

len(data.loc[:,'SECTION-LENGTH'][ctrl_ids]) / sum(data.loc[:,'SECTION-LENGTH'][ctrl_ids & auto_ids].unique())

SpineDensity = [None]*len(groups)
  
# retrieve section lengths of individual images
DendriticLength = np.array(data.loc[ctrl_ids & auto_ids,:].groupby('FileID')['SECTION-LENGTH'].unique())
for i in range(len(DendriticLength)):
    DendriticLength[i] = DendriticLength[i].sum() # sum each array withing the array of arrays
    
# number of spines per image
nSpines = np.array(data.loc[ctrl_ids,:].groupby('FileID').nunique()['ID'])   
# number of spines divided by dendritic length
SpineDensity = nSpines / DendriticLength

# spine morphology
# how many neck diameters is nan
len(data.loc[:,'NECK-DIAMETER'][np.isnan(data.loc[:,'NECK-DIAMETER']) == True]) / len(np.isnan(data.loc[:,'NECK-DIAMETER']))
data.loc[:,'NECK-DIAMETER'][np.isnan(data.loc[:,'NECK-DIAMETER']) == True] = 0 # get rid of nans

f, axs = plt.subplots(1,3)
nbins = 15
labels = ('CTRL','NMDAR')

# for currExpGroup in  groups:
#     for ind, val in enumerate(['HEAD-DIAMETER', 'NECK-DIAMETER', 'MAX-DTS']):
#             StuffToPlot = np.array(data.loc[:,val][data.loc[:,'ExpGroup'] == currExpGroup])
#             x = np.arange(StuffToPlot.min(), StuffToPlot.max(), 0.1)
#             y = StuffToPlot.cdf(x)
# stats.norm.cdf(StuffToPlot)
#             axs[ind].plot(x,y, '-')
        
 
StuffToPlot = [data.loc[:,'HEAD-DIAMETER'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'HEAD-DIAMETER'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[0].hist(StuffToPlot, bins=nbins, density=True, cumulative=False)    
axs[0].set_title('Head diameter')     
StuffToPlot = [data.loc[:,'NECK-DIAMETER'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'NECK-DIAMETER'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[1].hist(StuffToPlot, bins=nbins, density=True, cumulative=False)  
axs[1].set_title('Neck diameter')            
StuffToPlot = [data.loc[:,'MAX-DTS'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'MAX-DTS'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[2].hist(StuffToPlot, label=labels, bins=nbins, density=True, cumulative=False)   
axs[2].set_title('Spine length')           
f.legend()


# PCA and clustering analysis
f,ax = plt.subplots()
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data.loc[:,('HEAD-DIAMETER','NECK-DIAMETER', 'MAX-DTS')]) #,'SOMA-DISTANCE', 'XYPLANE-ANGLE')])

colorset = np.array(['red', 'orange', 'green', 'blue', 'magenta', 'gray', 'brown', 'black']*10)

dbscan = cluster.DBSCAN(eps=2.5, min_samples=10) 
dbscan.fit(data_pca) 
cids = dbscan.labels_ # get resulting cluster IDs from the kmeans object, one for each sample
colors = colorset[cids] # convert cluster IDs to colors

ax.scatter(data_pca[:, 0], data_pca[:, 1], color=colors) 
ax.set_title('PCA reduced data')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')




#for root, dirs, files in os.walk(path):
#   for name in files:
