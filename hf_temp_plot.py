"""
Vincent Andrews 

"""
import matplotlib.pyplot as plt
from astropy.io import fits 
import numpy as np
import math
import pandas as pd
import seaborn as sns
from operator import itemgetter
trot_vals = []
tkin_vals = []
hf_vals = []

def get_tkin(filepath):
    #getting hf_width file and storing in an array
    hdul = fits.open(filepath)
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none') 
    hdr.set('NAXIS3',1) 
    d = hdul[0].data 
    #swapping z and x axis 
    data = np.swapaxes(d,0,2)
    hdul.close()
    
    coords = []
    values = []
    for (i, j, k), value in np.ndenumerate(data):
        coords.append((i, j, k))
        values.append(value)
    df = pd.DataFrame({'Coordinate': coords, 'Value': values})
    df[['X', 'Y', 'Z']] = pd.DataFrame(df['Coordinate'].tolist(), index=df.index)
    df = df.drop('Coordinate', axis=1)
    DF = df.dropna() 
    DF = DF.drop(columns=["Z"])

    tkin = DF.Value.tolist()
    for t in tkin:
        tkin_vals.append(t)
    x = DF.X.tolist()
    y = DF.Y.tolist()
   
    return x,y

def get_hf(filepath,xlist,ylist):
    #getting hf_width file and storing in an array
    hdul = fits.open(filepath)
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none')  
    hdr.set('NAXIS3',1) 
    d = hdul[0].data 
    #swapping z and x axis 
    data = np.swapaxes(d,0,2)
    hdul.close()
    
    coords = []
    values = []
    for (i, j, k), value in np.ndenumerate(data):
        coords.append((i, j, k))
        values.append(value)
    df = pd.DataFrame({'Coordinate': coords, 'Value': values})
    df[['X', 'Y', 'Z']] = pd.DataFrame(df['Coordinate'].tolist(), index=df.index)
    df = df.drop('Coordinate', axis=1)
    DF = df.dropna() 
    DF = DF.drop(columns=["Z"])
 
    hf = DF.Value.tolist()
    x = DF.X.tolist()
    y = DF.Y.tolist()
    allhf = list(zip(x,y))

    hfv = []
    indx = 0

    for xi,yi in allhf:
        if indx == len(xlist):
            break
        if xi == xlist[indx] and yi == ylist[indx]:
            hfv.append(hf[indx])
            indx +=1
        else:
            continue 
    for hi in hfv:
        hf_vals.append(hi)
    return hfv

def get_trot(filepath):
    #getting hf_width file and storing in an array
    hdul = fits.open(filepath)
    hdr = hdul[0].header
    hdr.set('BLANCK', 'none') 
    hdr.set('NAXIS3',1) 
    d = hdul[0].data 
    #swapping z and x axis 
    data_array = np.swapaxes(d,0,2)
    
    for i in data_array:
        for j in i:
            for k in j:
                if math.isnan(float(k))==True:
                    continue 
                else:
                    trot_vals.append(k)
    hdul.close()
    print("Done with", filepath)
                    
L_file = ['L43']

for L in L_file:
    xc, yc = get_tkin('/home/scratch/vandrews/data/'+L+'_tkin.fits')
    get_hf('/home/scratch/vandrews/data/'+L+'_NH3_1-1_hf_width.fits', xc,yc)
    get_trot('/home/scratch/vandrews/data/'+L+'_trot.fits')
    
# hf_tkin = list(zip(hf_vals,tkin_vals))
# hf_trot = list(zip(hf_vals,trot_vals))
# data1 = sorted(hf_tkin,key=itemgetter(0))
# data2 = sorted(hf_trot,key=itemgetter(0))
# x1, y1 = zip(*data1)
# x2, y2 = zip(*data2)
sns.set_context('talk')
plt.style.use('dark_background')
c1 = 'cyan'
c2 = 'lime'
plt.scatter(hf_vals[::25],tkin_vals[::25],s = 8,color = c1,label ='kinetic temperature')
plt.scatter(hf_vals[::25],trot_vals[::25],s= 8,color = c2,label = 'rotational temperature')
plt.legend(loc = "upper left")
plt.xlabel("Hyperfine Width(km/s)")
plt.ylabel("Temperature(K)")
plt.title("Temperatures at Increasing Hyperfine Width")
figure = plt.gcf()
figure.set_size_inches(12,8)
plt.show()
plt.savefig('/home/scratch/vandrews/dataproducts/hf_vs_temp2.png',dpi = 100)
