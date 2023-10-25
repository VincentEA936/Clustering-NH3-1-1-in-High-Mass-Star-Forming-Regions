
"""
Created on Sat Jul 15 15:17:30 2023

@author: vandrews
"""

from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import statistics 
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
csfont = {'fontname':'Comic Sans MS'}
hfont = {'fontname':'Helvetica'}
plt.style.use('dark_background')

hf_vals = []
def get_hyperfine_values(filepath):
    print("Getting values for", filepath)
    hdul = fits.open(filepath)
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none') 
    hdr.set('NAXIS3',1) 
    d = hdul[0].data 
    data_array = np.swapaxes(d,0,2)
    hdul.close()
    #storing all values of interest in a list
    all_hf_values = []
    for i in data_array:
        for j in i:
            for k in j:
                if k == np.isnan:
                    pass
                else:
                    all_hf_values.append(k)
    nonan = [x for x in all_hf_values if str(x) != 'nan']
    for n in nonan:
        hf_vals.append(n)
  
    return 

L_file = ['L47','L43','L41','L40_5','L40','L39_5','L39','L38_5','L38','L37_5',
            'L37','L36_5','L36','L35_5','L35','L34_5','L34','L33_5','L33','L32_5'
            ,'L32','L31_5','L31','L30_5','L30','L29_5','L29','L28_5','L28','L27_5'
            ,'L27','L26_5','L26','L25_5','L25','L24_5','L24','L23_5','L23','L22_5'
            ,'L22','L21_5','L21','L20_5','L20','L19','L18_5','L18','L17_5','L17',
            'L16_5','L15_5','L15','L14_5','L14','L13_5','L13','L12_5','L12',
            'L11_5','L11','L10_5','L10']

for L in L_file:
    get_hyperfine_values('/home/scratch/vandrews/data/'+L+'_NH3_1-1_hf_width.fits')
cm = plt.cm.get_cmap('plasma')
mean_val = statistics.mean(hf_vals)
N, bins, patches = plt.hist(hf_vals, bins=80)
plt.axvline(x = 0.22, color = 'cyan', label = 'Hyperfine width in LTE = 0.22 km/s')
plt.axvline(x = mean_val, color = 'lime', label = 'Mean = 0.6481 km/s')
plt.xlabel('Hyperfine Width km/s',fontsize = 20)
plt.ylabel('Counts',fontsize = 20)
plt.title('Hyperfine Width PDF of Ammonia Inversion',fontsize = 30)
plt.legend(loc = "upper right",fontsize = 20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
bin_centers = 0.5 * (bins[:-1] + bins[1:])
col = bin_centers - min(bin_centers)
col /= max(col)
for c, p in zip(col, patches):
    plt.setp(p, 'facecolor', cm(c))
figure = plt.gcf()
figure.set_size_inches(12,8)
plt.savefig('/home/scratch/vandrews/dataproducts/hf_width_PDF.pdf',dpi = 100)