import os
import numpy as np
import pandas as pd 
solids = ['Cu', 'Ag', 'Pd', 'Rh', 'Li', 'Na', 'K', 'Rb', 'Cs', 
        'Ca', 'Sr', 'Ba', 'Al', 'LiF', 'LiCl', 'NaF', 'NaCl', 'MgO', 
        'C', 'SiC', 'Si', 'Ge', 'GaAs']

funcs = 'vdw-df',  'vdw-df-obk8',  'vdw-df-cx',   'vdw-df2', 'rev-vdw-df2', 'rvv10', 'new'

a_bohr = 0.529



from scipy.interpolate import lagrange

def construct_polynomial():
    Es_min = Es[ind-1:ind+2]
    ds_min = ds[ind-1:ind+2]
    poly = lagrange(ds_min, Es_min)
    return poly

def plot_test():
    pl.figure()
    pl.plot(ds,Es,'o')
    pl.plot(d_dense,E_dense)
    pl.xlim(min(d_dense),max(d_dense))
    delta = max(E_dense) - min(E_dense)
    pl.ylim(min(E_dense)-0.1*delta, max(E_dense))
    pl.plot(d_min,E_min,marker='x',color='r',markersize=20,markeredgewidth=1)
    pl.savefig('figures'+'/'+ solid +'_' +  fun + '.png')
#    pl.show()

import pylab as pl


d_data = pl.zeros((len(solids), len(funcs)))

E_data = pl.zeros((len(solids), len(funcs)))

for i, solid in enumerate(solids):
 #   os.chdir(solid)
    for j, fun in enumerate(funcs):

        print solid, fun  
        
        path = solid + '/' + fun

        data = np.loadtxt(path+'/energy_vs_lattice.txt')
        ds = data[:,0]*a_bohr

        Es = data[:,1]
        ind = np.argmin(Es)

        d_dense = np.linspace(ds[ind-2],ds[ind+3], 50)
        poly = construct_polynomial()
        
        E_dense = poly(d_dense)
        ind_min = np.argmin(poly(d_dense))

        d_min = d_dense[ind_min]
        E_min = poly(d_min)

        plot_test()
	
	d_data[i,j] = d_min
        E_data[i,j] = E_min
  
        print solid, fun, E_min

df = pd.DataFrame(data = d_data, columns = funcs, index=solids)
print df
df.to_excel('dist.xls')   

df = pd.DataFrame(data = E-data, columns = funcs, index=solids)
print df
df.to_excel('Energy.xls')   




