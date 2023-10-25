'''
Vincent Andrews

This code computes the average kinetic temperature of ammonia
in all regions of the survey.
This value is then used for calculating the expected thermal dispersion 
across the entire region surveyed

Result: 0.22 km/s (calculations not shown here) for Tkin = avg_tkin 
'''
from astropy.io import fits
import numpy as np
import statistics 

tkin_vals = []
def get_tkin_values(filepath):
    print("Getting values for", filepath)
    #getting hf_width file and storing in an array
    hdul = fits.open(filepath)
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none') 
    hdr.set('NAXIS3',1) 
    d = hdul[0].data 
    #swapping z and x axis 
    data_array = np.swapaxes(d,0,2)
    hdul.close()
    #storing all values of interest in a list
    all_tkin_values = []
    for i in data_array:
        for j in i:
            for k in j:
                if k == np.isnan:
                    pass
                else:
                    all_tkin_values.append(k)
    #removing nan values
    nonan = [x for x in all_tkin_values if str(x) != 'nan']
    for n in nonan:
        tkin_vals.append(n)
#list of regions based on file naming scheme
L_file = ['L43','L41','L40_5','L40','L39_5','L39','L38_5','L38','L37_5',
            'L37','L36_5','L36','L35_5','L34_5','L34','L33_5','L33','L32_5'
            ,'L32','L31_5','L31','L30_5','L30','L29_5','L29','L28_5','L28','L27_5'
            ,'L27','L26_5','L26','L25_5','L25','L24_5','L24','L23_5','L23','L22_5'
            ,'L22','L21_5','L21','L20_5','L20','L19','L18_5','L18','L17_5','L17',
            'L16_5','L15_5','L15','L14_5','L14','L13_5','L13','L12_5','L12',
            'L11_5','L11','L10_5','L10']

for L in L_file:
    get_tkin_values('/home/scratch/vandrews/data/'+L+'_tkin.fits')

avg_tkin = statistics.mean(tkin_vals)