'''
Vincent Andrews 

This script calculates the average hyperfine velocity at local standard 
of rest and the error in this velocity for each region of the 
RAMPS data 

These lists are then imnported into the clump_distances script for estimnating 
distances to the center of each region
'''
from astropy.io import fits
import numpy as np
import statistics 

VLSR = []
VERR = []
def get_vel_values(filepath):
    hdul = fits.open('/home/scratch/vandrews/data/'+filepath+'_NH3_1-1_hf_vel.fits')
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none') 
    hdr.set('NAXIS3',1) 
    d = hdul[0].data 
    data_array = np.swapaxes(d,0,2)
    hdul.close()
    all_vel_values = []
    for i in data_array:
        for j in i:
            for k in j:
                if k == np.isnan:
                    pass
                else:
                    all_vel_values.append(k)
    nonan = [x for x in all_vel_values if str(x) != 'nan']
    mean_vel = statistics.mean(nonan)
    
    hdul = fits.open('/home/scratch/vandrews/data/'+filepath+'_NH3_1-1_hf_vel_err.fits')
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none') 
    hdr.set('NAXIS3',1) 
    d = hdul[0].data 
    data_array = np.swapaxes(d,0,2)
    hdul.close()
    all_err_values = []
    for i in data_array:
        for j in i:
            for k in j:
                if k == np.isnan:
                    pass
                else:
                    all_err_values.append(k)
    nonan2 = [x for x in all_err_values if str(x) != 'nan']
    mean_err = statistics.mean(nonan2)
    return mean_vel, mean_err

L_file = ['L43','L41','L40_5','L40','L39_5','L39','L38_5','L38','L37_5',
            'L37','L36_5','L36','L35_5','L34_5','L34','L33_5','L33','L32_5'
            ,'L32','L31_5','L31','L30_5','L30','L29_5','L29','L28_5','L28','L27_5'
            ,'L27','L26_5','L26','L25_5','L25','L24_5','L24','L23_5','L23','L22_5'
            ,'L22','L21_5','L21','L20_5','L20','L19','L18_5','L18','L17_5','L17',
            'L16_5','L15_5','L15','L14_5','L14','L13_5','L13','L12_5','L12',
            'L11_5','L11','L10_5']
for L in L_file:
     print("getting velocity data for", L)
     VEL,ERR = get_vel_values(L)
     VLSR.append(VEL)
     VERR.append(ERR)