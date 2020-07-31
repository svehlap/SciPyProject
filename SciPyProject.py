# SciPy project by Pavel Svehla

# this script processes csv files generated by a software called Neuronstdio, in which dendritic spines in confocal images were manually reconstructed. 
# the aim of the experiment is to see whether pathogenic antibodies isolated from patients affect neuronal morphology, namely post-synapses.
# mice were chronicly infused with these antibodies targeting NMDAR and cauing its downregulation. There are two groups: control antibody and NMDAR antibody.
# Data is organized in folder 'data' containing subfolders representing the experimental groups, each group contains subfolders representing a mouse.


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from os import listdir
from os.path import isfile, isdir, join
import scipy.stats as stats
from sklearn.decomposition import PCA
from sklearn import cluster

data = pd.DataFrame() # initialize a dataframe to append data to it

mypath = join(os.path.dirname(__file__), 'data') 

##### get the data
groups = [f for f in listdir(mypath)]
for group in groups:
    
    subfolders = [f for f in listdir(join(mypath, group))] # extraxt folder names
    for subfolder in subfolders: # extract subfolder names
        files = [f for f in listdir(join(mypath, group, subfolder))]
        for file in files: # extract files from subfolders
            data_tmp = pd.read_csv(join(mypath, group, subfolder, file))
            
            # add more columns to the data
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
                        
            data = data.append(data_tmp) # combine in one big dataframe


############## analysis
# print some output
print('total of %i spines were counted in %i images' %(len(data), len(data.groupby('FileID'))))

# spine density
auto_ids = data.loc[:,'AUTO'] == 'yes' # indexes to automatic spines, manual spines are problematic (incorrect data)
SpineDensity = [None]*len(groups)
for group_ind, group in enumerate(groups): 
    group_ids = data.loc[:,'ExpGroup'] == group
    # retrieve section lengths of individual images
    DendriticLength = np.array(data.loc[group_ids & auto_ids,:].groupby('FileID')['SECTION-LENGTH'].unique())
    for i in range(len(DendriticLength)):
        DendriticLength[i] = DendriticLength[i].sum() # sum each array withing the array of arrays
        
    # number of spines per image
    nSpines = np.array(data.loc[group_ids,:].groupby('FileID').nunique()['ID'])   
    # number of spines divided by dendritic length
    SpineDensity[group_ind] = nSpines / DendriticLength

# do a t test and print the result
t,p = stats.ttest_ind(SpineDensity[0], SpineDensity[1])
print('t-test p-value is %g' %(p))


#SpineDensityAv = [] 
#for i in range(len(SpineDensity)):
#    SpineDensityAv = SpineDensityAv.append(np.mean(SpineDensity[i]))
    
############## plots
# spine morphology
data.loc[:,'NECK-DIAMETER'][np.isnan(data.loc[:,'NECK-DIAMETER']) == True] = 0 # get rid of nans

f, axs = plt.subplots(1,3)
nbins = 15
 
StuffToPlot = [data.loc[:,'HEAD-DIAMETER'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'HEAD-DIAMETER'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[0].hist(StuffToPlot, bins=nbins, density=True, cumulative=False)    
axs[0].set_title('Head diameter')
axs[0].set_xlabel('um')    
StuffToPlot = [data.loc[:,'NECK-DIAMETER'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'NECK-DIAMETER'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[1].hist(StuffToPlot, bins=nbins, density=True, cumulative=False)  
axs[1].set_title('Neck diameter')            
axs[1].set_xlabel('um')
StuffToPlot = [data.loc[:,'MAX-DTS'][data.loc[:,'ExpGroup'] == 'CTRL'], data.loc[:,'MAX-DTS'][data.loc[:,'ExpGroup'] == 'NMDAR']]
axs[2].hist(StuffToPlot, label=groups, bins=nbins, density=True, cumulative=False)   
axs[2].set_title('Spine length')           
axs[2].set_xlabel('um')
f.legend()
plt.savefig('histograms.png')

# PCA and clustering analysis
f,ax = plt.subplots()
pca = PCA(n_components=2)
data_pca = pca.fit_transform(data.loc[:,('HEAD-DIAMETER','NECK-DIAMETER', 'MAX-DTS','SOMA-DISTANCE', 'XYPLANE-ANGLE')]) # subset meaningful data

colorset = np.array(['red', 'orange', 'green', 'blue', 'magenta', 'gray', 'brown', 'black']*10)

dbscan = cluster.DBSCAN(eps=2.5, min_samples=1000) 
dbscan.fit(data_pca) 
cids = dbscan.labels_ # get resulting cluster IDs from the kmeans object, one for each sample
colors = colorset[cids] # convert cluster IDs to colors

ax.scatter(data_pca[:, 0], data_pca[:, 1], color=colors) 
ax.set_title('PCA reduced data')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
plt.savefig('PCA.png')
