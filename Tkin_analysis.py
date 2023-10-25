"""
Vincent Andrews 
Kinetic Temperature Analysis 
    # This code imports the initial centroid identifications from the kmeans
    algorithim and checks the kinetic temperature in those regions 
    # The regions are then either passed as possible regions of 
    early star formation or ignored in the new dictionary 
    # we can then re visualize the scatterplot of coordinates and see which 
    regions remain on the plot 
"""
#import kmeans clustering script results to access target coordinates
#once opened, you can access any variable by typing KM.variablename
import Kmeans_clumpfinder as KM

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import statistics 
import matplotlib as mpl
import pandas as pd

def Open_file(path):
    hdul = fits.open('/home/scratch/vandrews/data/'+L+'_tkin.fits')
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none') # idk why blanck = -1 originally 
    hdr.set('NAXIS3',1) #i get an error message when this is gone idk
    d = hdul[0].data #3D with 2 channels ?
    data = np.swapaxes(d,0,2)

    coords = []
    values = []
    for (i, j, k), value in np.ndenumerate(data):
        coords.append((i, j, k))
        values.append(value)
    df = pd.DataFrame({'Coordinate': coords, 'Value': values})
    df[['X', 'Y', 'Z']] = pd.DataFrame(df['Coordinate'].tolist(), index=df.index)
    df = df.drop('Coordinate', axis=1)
    DF = df.dropna() #removing nan values 

    tkin1 = DF[(DF['Value'] <= 20)]  
    tkin2 = tkin1.drop(columns=["Z","Value"])
    #note-has the index corresponding to the initial position in the raw data
    Ltkin = tkin2.reset_index(drop = True) #Ltkin = low kinetic temperature 
    return Ltkin,tkin1

def check_tkin(num):
    #get coordinates from dictionary 
    X_list = Cord_dict['Xcord'+str(num)]
    Y_list = Cord_dict['Ycord'+str(num)]
    
    tkin_vals = []
    bad_regions = []
    j = 0
    while j <= len(X_list):
        val = tkin_df[(tkin_df["X"]==X_list[j]) & 
                           (tkin_df["Y"]==Y_list[j]) & (tkin_df["Z"]==0)]["Value"]
        tkin_vals.append(val)
        avg = statistics.mean(tkin_vals)
        if avg > 20:
            bad_regions.append(j)
            j = j+1
        else:
            j=j+1
    return bad_regions
'''
Part 1: Get kmeans file variables
    # make sure file is run before this 
'''
Cord_dict = KM.coordinate_dictionary
n_clusters = KM.n_clusters 

'''
Part 2: Open Tkin files from RAMPS derived data products
'''
L = 'L14_5' #make sure path here matches up with other file
Ltkin_df,tkin_df = Open_file(L) #low tkin dataframe 
    
'''
Part 3: Check tkin using function call
'''
i = 0
while i <= n_clusters:
    bad_clumps = check_tkin(i)
    i = i + 1
print(bad_clumps)