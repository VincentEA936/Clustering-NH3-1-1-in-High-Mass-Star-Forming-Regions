import pandas as pd
from astropy.io import fits
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from tqdm import tqdm #for timing loops
from time import sleep 
import statistics 
import scipy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
csfont = {'fontname':'Comic Sans MS'}
hfont = {'fontname':'Helvetica'}
import matplotlib as mpl
import statistics 
import sys 

def get_hyperfine_values(filepath):
    print("Getting values for", filepath)
    #getting hf_width file and storing in an array
    hdul = fits.open(filepath)
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none') # idk why blanck = -1 originally 
    hdr.set('NAXIS3',1) #i get an error message when this is gone idk
    d = hdul[0].data #3D with 2 channels ?
    #swapping z and x axis 
    data_array = np.swapaxes(d,0,2)
    
    #storing all values of interest in a list
    all_hf_values = []
    for i in data_array:
        for j in i:
            for k in j:
                if k == np.isnan:
                    pass
                else:
                    all_hf_values.append(k)
    print("Calculating maximum value and standard deviation")
    #removing nans reduces plotting time 
    nonan = [x for x in all_hf_values if str(x) != 'nan']
    mean_val = statistics.mean(nonan)
    stdev = statistics.stdev(nonan)
    
    round_stdev= round(stdev, 3)
    stats = '\n'.join([
        '{:<8}{:>4.2f}'.format('Mean:', mean_val),
        '{:<8}{:>4.2f}'.format('SD:', stdev),
    ])
    return nonan, mean_val, round_stdev, stats

#calling function to import data from select file path
#L19_5 to L10
L_file = ['L19','L18_5','L18','L17_5','L17','L16_5','L15_5','L15','L14_5','L14',
          'L13_5','L13','L12_5','L12','L11_5','L11','L10_5','L10']

low_hf_19_5, mean19_5, stdev19_5, stats19_5 = get_hyperfine_values('/home/scratch/vandrews/data/L19_NH3_1-1_hf_width(1).fits')
low_hf_19, mean19, stdev19, stats19 = get_hyperfine_values('/home/scratch/vandrews/data/L19_NH3_1-1_hf_width.fits')
low_hf_18_5, mean18_5, stdev18_5, stats18_5 = get_hyperfine_values('/home/scratch/vandrews/data/L18_5_NH3_1-1_hf_width.fits')
low_hf_18, mean18, stdev18, stats18 = get_hyperfine_values('/home/scratch/vandrews/data/L18_NH3_1-1_hf_width.fits')
low_hf_17_5, mean17_5, stdev17_5, stats17_5 = get_hyperfine_values('/home/scratch/vandrews/data/L17_5_NH3_1-1_hf_width.fits')
low_hf_17, mean17, stdev17, stats17 = get_hyperfine_values('/home/scratch/vandrews/data/L17_NH3_1-1_hf_width.fits')
low_hf_16_5, mean16_5, stdev16_5, stats16_5 = get_hyperfine_values('/home/scratch/vandrews/data/L16_5_NH3_1-1_hf_width.fits')
#low_hf_16 = get_hyperfine_values('/home/scratch/vandrews/data/L16_NH3_1-1_hf_width.fits')
low_hf_15_5, mean15_5, stdev15_5, stats15_5 = get_hyperfine_values('/home/scratch/vandrews/data/L15_5_NH3_1-1_hf_width.fits')
low_hf_15, mean15, stdev15, stats15 = get_hyperfine_values('/home/scratch/vandrews/data/L14_NH3_1-1_hf_width.fits')
low_hf_14_5, mean14_5, stdev14_5, stats14_5 = get_hyperfine_values('/home/scratch/vandrews/data/L14_5_NH3_1-1_hf_width.fits')


COLOR = 'black'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
cm = plt.cm.get_cmap('plasma')
fig, axs = plt.subplots(2, 5, figsize = (34,18), sharex = 'none')
fig.patch.set_facecolor('white')
fig.suptitle("Hyperfine Width Probability Distribution Function", x= 0.52, y =0.95, 
                     fontsize = 40, 
                     fontweight = "bold",
                     **csfont)
custom_box = dict(boxstyle='round', facecolor='white', alpha=0.5)
#1
N, bins, patches = axs[0,0].hist(low_hf_19_5, bins=30)
axs[0,0].set_title('Region L19_5', fontsize = 25, **csfont,fontweight = "bold")
axs[0,0].text(0.9,0.9,stats19_5, bbox = custom_box, 
              horizontalalignment='right', verticalalignment='top', 
              transform = axs[0,0].transAxes, fontsize = 25)
axs[0,0].axvline(x = mean19_5, color = 'pink', label = 'Mean')
axs[0,0].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#2
N, bins, patches = axs[0,1].hist(low_hf_19, bins=30)
axs[0,1].set_title('Region L19', fontsize = 25, **csfont,fontweight = "bold")
axs[0,1].text(0.8,0.85,stats19, bbox = custom_box, 
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[0,1].transAxes, fontsize = 25)
axs[0,1].axvline(x = mean19, color = 'pink', label = 'Mean')
axs[0,1].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#3
N, bins, patches = axs[0,2].hist(low_hf_18_5, bins=30)
axs[0,2].set_title('Region L18_5', fontsize = 25, **csfont,fontweight = "bold")
axs[0,2].text(0.8,0.85,stats18_5, bbox = custom_box,
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[0,2].transAxes, fontsize = 25)
axs[0,2].axvline(x = mean18_5, color = 'pink', label = 'Mean')
axs[0,2].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#4
N, bins, patches = axs[0,3].hist(low_hf_18, bins=30)
axs[0,3].set_title('Region L18', fontsize = 25, **csfont,fontweight = "bold")
axs[0,3].text(0.8,0.85,stats18, bbox = custom_box,
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[0,3].transAxes, fontsize = 25)
axs[0,3].axvline(x = mean18, color = 'pink', label = 'Mean')
axs[0,3].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#5
N, bins, patches = axs[0,4].hist(low_hf_17_5, bins=30)
axs[0,4].set_title('Region L17_5', fontsize = 25, **csfont,fontweight = "bold")
axs[0,4].text(0.8,0.85,stats17_5, bbox = custom_box,
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[0,4].transAxes, fontsize = 25)
axs[0,4].axvline(x = mean17_5, color = 'pink', label = 'Mean')
axs[0,4].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#6
N, bins, patches = axs[1,0].hist(low_hf_17, bins=30)
axs[1,0].set_title('Region L17', fontsize = 25, **csfont,fontweight = "bold")
axs[1,0].text(0.8,0.85,stats17, bbox = custom_box,
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[1,0].transAxes, fontsize = 25)
axs[1,0].axvline(x = mean17, color = 'pink', label = 'Mean')
axs[1,0].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#7
N, bins, patches = axs[1,1].hist(low_hf_16_5, bins=30)
axs[1,1].set_title('Region L16_5', fontsize = 25, **csfont,fontweight = "bold")
axs[1,1].text(0.8,0.85,stats16_5, bbox = custom_box,
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[1,1].transAxes, fontsize = 25)
axs[1,1].axvline(x = mean16_5, color = 'pink', label = 'Mean')
axs[1,1].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#8
N, bins, patches = axs[1,2].hist(low_hf_15_5, bins=30)
axs[1,2].set_title('Region L15_5', fontsize = 25, **csfont,fontweight = "bold")
axs[1,2].text(0.8,0.85,stats15_5, bbox = custom_box,
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[1,2].transAxes, fontsize = 25)
axs[1,2].axvline(x = mean15_5, color = 'pink', label = 'Mean')
axs[1,2].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#9   
N, bins, patches = axs[1,3].hist(low_hf_15, bins=30)
axs[1,3].set_title('Region L15', fontsize = 25, **csfont,fontweight = "bold")
axs[1,3].text(0.8,0.85,stats15, bbox = custom_box,
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[1,3].transAxes, fontsize = 25)
axs[1,3].axvline(x = mean15, color = 'pink', label = 'Mean')
axs[1,3].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
#10
N, bins, patches = axs[1,4].hist(low_hf_14_5, bins=30)
axs[1,4].set_title('Region L14_5', fontsize = 25, **csfont,fontweight = "bold")
axs[1,4].text(0.8,0.85,stats14_5, bbox = custom_box,
              horizontalalignment='center', verticalalignment='center', 
              transform = axs[1,4].transAxes, fontsize = 25)
axs[1,4].axvline(x = mean14_5, color = 'pink', label = 'Mean')
axs[1,4].set_facecolor("white")
bin_centers = 0.5 * (bins[:-1] + bins[1:])
# scale values to interval [0,1]
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
    
for ax in axs.flat:
    ax.set(xlabel='Hyperfine Width (m/s)', ylabel='Number of Pixels')
    ax.xaxis.label.set_size(32) 
    ax.yaxis.label.set_size(32) 
    ax.xaxis.set_tick_params(labelsize=20,width = 2, labelcolor = 'black')
    ax.yaxis.set_tick_params(labelsize=20, width = 2,labelcolor = 'black')
for ax in axs.flat:
    ax.label_outer()
    
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', fontsize = "40", facecolor = 'white')
#plt.savefig('/home/scratch/vandrews/figures/test_plot2.pdf')

