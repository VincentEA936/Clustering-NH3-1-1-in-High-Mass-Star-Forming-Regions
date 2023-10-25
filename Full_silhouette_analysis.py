"""
Vinny Andrews 
"""
'''
Using Silhouette Score Analysis for finding the optimal number of clusters for 
K-means clustering:
     # This code opens a selected group of hyperfine width maps as fits files
     and exports the data using astropy
     # K-means is performed on all regions for different numbers of clusters,
     i chose 2-120 here for good measure(must be greateer than 1 for first one)
     # each k(number of clusters) is initialized 1000 times, improving accuracy 
     with higher iterations(also increasing run time)
     # Each region is plotted with number of clusters on the x axis and silhouette 
     score on the y-axis 
     # interpretation/analysis: the highest silhouette score will be the best 
     cluster number init for each region; however, if the plot plateaus after 
     a certain value, choose the value right before the plateau
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits #opens fits files
from sklearn.cluster import KMeans #clustering algorithim
from sklearn.metrics import silhouette_score #calculates silhouette scores
'''
Part 1: Setting up subplot and function
    #This plots the silhouette score with the number of clusters on 
    the x-axis.The peak is generally taken as the best init of k-means 
'''
fig, axs = plt.subplots(3,5, figsize = (34,18), sharex = 'none')
fig.suptitle("Silhouette Scores for K-Means Clustering", 
             x= 0.52, y =0.95, fontsize = 40, fontweight = "bold")
fig2, axs2 = plt.subplots(4,4, figsize = (36,24), sharex = 'none')
fig.suptitle("Silhouette Scores for Cluster Initializations", 
             x= 0.52, y =0.95, fontsize = 40, fontweight = "bold")
fig3, axs3 = plt.subplots(4,4, figsize = (36,24), sharex = 'none')
fig.suptitle("Silhouette Scores for Cluster Initializations", 
             x= 0.52, y =0.95, fontsize = 40, fontweight = "bold")
fig4, axs4 = plt.subplots(4,4, figsize = (36,24), sharex = 'none')
fig.suptitle("Silhouette Scores for Cluster Initializations", 
             x= 0.52, y =0.95, fontsize = 40, fontweight = "bold")
#this sets axes only on the outter sub plots
for ax in axs.flat:
    ax.set(xlabel='Number of Clusters', ylabel='Silhouette Score')
    ax.xaxis.label.set_size(28) 
    ax.yaxis.label.set_size(28) 
    ax.xaxis.set_tick_params(labelsize=20,width = 2, labelcolor = 'black')
    ax.yaxis.set_tick_params(labelsize=20, width = 2,labelcolor = 'black')   
for ax in axs.flat:
    ax.label_outer()
for ax in axs2.flat:
    ax.set(xlabel='Number of Clusters', ylabel='Silhouette Score')
    ax.xaxis.label.set_size(28) 
    ax.yaxis.label.set_size(28) 
    ax.xaxis.set_tick_params(labelsize=20,width = 2, labelcolor = 'black')
    ax.yaxis.set_tick_params(labelsize=20, width = 2,labelcolor = 'black')    
for ax in axs2.flat:
      ax.label_outer()
for ax in axs3.flat:
    ax.set(xlabel='Number of Clusters', ylabel='Silhouette Score')
    ax.xaxis.label.set_size(28) 
    ax.yaxis.label.set_size(28) 
    ax.xaxis.set_tick_params(labelsize=20,width = 2, labelcolor = 'black')
    ax.yaxis.set_tick_params(labelsize=20, width = 2,labelcolor = 'black')   
for ax in axs3.flat:
    ax.label_outer()
for ax in axs4.flat:
    ax.set(xlabel='Number of Clusters', ylabel='Silhouette Score')
    ax.xaxis.label.set_size(28) 
    ax.yaxis.label.set_size(28) 
    ax.xaxis.set_tick_params(labelsize=20,width = 2, labelcolor = 'black')
    ax.yaxis.set_tick_params(labelsize=20, width = 2,labelcolor = 'black')    
for ax in axs4.flat:
      ax.label_outer()
    
def open_file(path):
    filepath = ('/home/scratch/vandrews/data/'+L+'_NH3_1-1_hf_width.fits')
    #print("Opening hyperfine width data for region...", L) #using hyperfine map
    hdu = fits.open(filepath)
    hdr = hdu[0].header
    hdr.set('BLANCK', 'none') 
    hdr.set('NAXIS3',1)
    hdr.set('CUNIT3','m/s')
    d = hdu[0].data 
    data = np.swapaxes(d,0,2) #(x,y,x) z is channel 
    
    coords = []
    values = []
    for (i, j, k), value in np.ndenumerate(data):
        coords.append((i, j, k)) 
        values.append(value)
    df = pd.DataFrame({'Coordinate': coords, 'Value': values})
    df[['X', 'Y', 'Z']] = pd.DataFrame(df['Coordinate'].tolist(), index=df.index)
    df_raw = df.drop('Coordinate', axis=1) #raw hyperfine dataframe 
    #print("Removing NaN values and reducing hyperfine data for region...",L)
    DF = df_raw.dropna() #remove nan
    lowHF = DF[(DF['Value'] <= 0.25)]

    lowHF_XY = lowHF.drop(columns = ['Value', 'Z']) #just want xy cords 

    return lowHF_XY

#score list, num clusters, subplot location, region number, figure num
def silhouette_plot(s_scores, k, row, col,l,N):
    if N == 1:
        axs[row,col].plot(k,s_scores,color = 'purple',linewidth = '5')
        axs[row,col].set_title('Region'+l, fontsize = 25,fontweight = "bold")
    elif N == 2:
        axs2[row,col].plot(k,s_scores,color = 'purple',linewidth = '5')
        axs2[row,col].set_title('Region'+l, fontsize = 25,fontweight = "bold")
    elif N == 3:
        axs3[row,col].plot(k,s_scores,color = 'purple',linewidth = '5')
        axs3[row,col].set_title('Region'+l, fontsize = 25,fontweight = "bold")
    elif N == 4:
        axs4[row,col].plot(k,s_scores,color = 'purple',linewidth = '5')
        axs4[row,col].set_title('Region'+l, fontsize = 25,fontweight = "bold")
'''
Part 2: Select regions of interest from data 
'''
#list of hyperfine width maps from the RAMPS data
L_file = ['L47','L43','L41','L40_5','L40','L39_5','L39','L38_5','L38','L37_5',
          'L37','L36_5','L36','L35_5','L35','L34_5','L34','L33_5','L33','L32_5'
          ,'L32','L31_5','L31','L30_5','L30','L29_5','L29','L28_5','L28','L27_5'
          ,'L27','L26_5','L26','L25_5','L25','L24_5','L24','L23_5','L23','L22_5'
          ,'L22','L21_5','L21','L20_5','L20','L19','L18_5','L18','L17_5','L17',
          'L16_5','L15_5','L15','L14_5','L14','L13_5','L13','L12_5','L12',
          'L11_5','L11','L10_5','L10']

#lists of all positions in the subplot
rows = [0,0,0,0,0,1,1,1,1,1,2,2,2,2,2]      
cols = [0,1,2,3,4,0,1,2,3,4,0,1,2,3,4]
     
rows2 = [0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3]
cols2 = [0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3]

clusters = [] #this list gets the maximum value of each plot(NOTE: this may not
              #always be the best K-means init if the plot plateaus)
fn = 1
subplot_index = 0
for L in L_file:
    '''
    Part 3: Data reduction to low hyperfine width regions
    '''
    data = open_file(L)
    silhouette_scores = [] #list of scores that are plotted on the y-axis 
    n_clusters_best = []
    '''
    Part 4: Silhouette analysis 
    '''
    print("Performing Silhouette analysis for region...",L)
    if (L == 'L47' or L == 'L43' or L == 'L41' or L == 'L40_5' or L == 'L40' 
    or L == 'L39_5' or L == 'L34' or L == 'L22_5' or L == 'L20' ):
        n_clusters = list(range(2,17))
        max_n = len(n_clusters)+1
    else:
        n_clusters = list(range(2,100)) 
        max_n = len(n_clusters)+1
    q = 2
    while q <= max_n:
        #using kmeans++ : speeds up convergence by empirically selecting 
        #centroids based on the probability distribution function 
        km = KMeans(n_clusters=q,init='k-means++',n_init = 100)
        km.fit(data)
        labels = km.predict(data)
        #getting Silhouette scores
        sc = silhouette_score(data,labels, metric = 'euclidean')
        print("Silhouette Score n =",q,":", sc)
        silhouette_scores.append(sc)
        n_clusters_best.append(q)
        q = q + 1
    if subplot_index == 15 and (fn == 1):
        subplot_index = 0
        fn = fn + 1
    elif subplot_index == 16 and (fn == 2,3,4):
        subplot_index = 0
        fn = fn +1
        
    if fn == 1:
        row_index = rows[subplot_index] #row/col index
        col_index = cols[subplot_index]
    else:
        row_index = rows2[subplot_index]
        col_index = cols2[subplot_index]
    
    #Max value is not alwyas the best!!!
    #gets index of max value in scores list
    max_index = silhouette_scores.index(max(silhouette_scores))
    #best cluster number is at same index
    best_num = n_clusters_best[max_index]
    #appends best cluster number to a list for each region
    clusters.append(best_num)
    '''
    Part 5: Calling function to plot socres
    '''
    silhouette_plot(silhouette_scores, n_clusters,row_index, col_index,L,fn)
    subplot_index = subplot_index + 1
'''
Analysis: max number of scores is not the best score for most of the plots
    - Likely because clusters are being split into many new clusters with 
    higher number of cluster initilizations 
    - some have well defined peaks where the max can be taken
    - need to look at hyperfine map for each one otherwise and take a rough
    estimate 
    - best number is probably right before the line starts to plateau out
'''
'''
    #final number of clusters for kmeans (for now)
    #i would like to adjust the paramaters to improve the convergence accuracy
    #NOTE- Regions marked below are ones that had bad silhouette analysis runs 
    L41,L40_5,L40,L39_5(really bad),L36(maybe too much),L34(wayy too little),
    L31_5(data being very spread out might make it harder), 
    L31,L30_5,L30,L29_5(potentially more),L29(prob more,data sparse),L28_5(prob more),
    L28(oversamp - reduced to 60),L27_5(2 peaks, first one is fine),
    L27(too much, prob 20-40), L26_5(i guess 98.. maybe more), L25(maybe more),
    L20 (more), L19(more),L13_5 (interesting structure,bad sc),
    L13 (large filament)
    *L13,L13_5 have large structures, not sure how kmeans will cluster stuff
    try with different scores and see what happens
    L12_5- another large structure
    L12, L11_5,L10_5 - more large structures
    L11 - snake dark cloud
'''
final_nums = [5,16,2,2,2,2,23,26,26,26,26,42,62,40,41,
              41,3,25,19,15,69,50,93,89,93,80,39,92,60,40,30
              ,98,35,39,88,80,93,92,99,9,6,17,19,11,16,84,74,
              49,2,5,33,41,8,60,60,40,35,35,50,30,18,40,40,20]