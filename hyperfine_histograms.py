'''
Vinny Andrews 
'''
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import statistics 

csfont = {'fontname':'Comic Sans MS'}
hfont = {'fontname':'Helvetica'}
import matplotlib as mpl

def get_hyperfine_values(filepath,row,col,L):
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
        '{:<8}{:>4.2f}'.format('SD:', stdev)])
    r = row
    c = col
    L = L
  
    plot_histogram(nonan, mean_val, round_stdev, stats, r, c,L)
    return nonan, mean_val, round_stdev, stats

def plot_histogram(d, m, sig, stat,row,col,L):
    N, bins, patches = axs[row,col].hist(d, bins=30)
    axs[row,col].set_title('Region'+L, fontsize = 25, **csfont,fontweight = "bold")
    axs[row,col].text(0.9,0.9,stat, bbox = custom_box, 
                         horizontalalignment='right', verticalalignment='top', 
                         transform = axs[row,col].transAxes, fontsize = 25)
    axs[row,col].axvline(x = m, color = 'pink', label = 'Mean')
    axs[row,col].axvline(x = 0.10, color = 'cyan', label = 'lowHF')
    axs[row,col].set_facecolor("white")
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    # scale values to interval [0,1]
    col = bin_centers - min(bin_centers)
    col /= max(col)
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
   
#define list of regions 
L_region = ['L19','L18_5','L18','L17_5','L17','L16_5','L15_5','L15','L14_5','L14',
          'L13_5','L13','L12_5','L12','L11_5','L11','L10_5','L10']

#initialize plot size 
n = 3 #rows
m = 6 #cols
#customizing subplot appearance   
COLOR = 'black'
mpl.rcParams['text.color'] = COLOR
mpl.rcParams['axes.labelcolor'] = COLOR
mpl.rcParams['xtick.color'] = COLOR
mpl.rcParams['ytick.color'] = COLOR
cm = plt.cm.get_cmap('plasma')
#creating subplot axes
fig, axs = plt.subplots(n, m, figsize = (34,18), sharex = 'none')
fig.suptitle("Hyperfine Width Probability Distribution Function", 
             x= 0.52, y =0.95, fontsize = 40, 
             fontweight = "bold", **csfont)
custom_box = dict(boxstyle='round', facecolor='white', alpha=0.5)

#list of positions on subplot 
ax1 = [0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,2]
ax2 = [0,1,2,3,4,5,0,1,2,3,4,5,0,1,2,3,4,5]
index = 0
for L in L_region:
    r = ax1[index]
    c = ax2[index]
    get_hyperfine_values('/home/scratch/vandrews/data/'+L+'_NH3_1-1_hf_width.fits',r,c,L)    
    index = index + 1
for ax in axs.flat:
    ax.set(xlabel='Hyperfine Width (km/s)', ylabel='Number of Pixels')
    ax.xaxis.label.set_size(28) 
    ax.yaxis.label.set_size(28) 
    ax.xaxis.set_tick_params(labelsize=20,width = 2, labelcolor = 'black')
    ax.yaxis.set_tick_params(labelsize=20, width = 2,labelcolor = 'black')
    
for ax in axs.flat:
    ax.label_outer()
    
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', fontsize = "30", facecolor = 'white')
plt.show()