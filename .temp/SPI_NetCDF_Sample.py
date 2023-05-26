from distributed import Client
#client = Client(n_workers=4, threads_per_worker=1, memory_limit='5GB')

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import xarray as xr
import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plt
#%matplotlib inline

# Standardized Precipitation Index Function
def spi(ds, thresh, dimension):
    # ds - data ; thresh - time interval / scale; dimension - dimension as a string

    # Rolling Mean / Moving Averages
    ds_ma = ds.rolling(time=thresh, center=False).mean(dim=dimension)

    # Natural log of moving averages
    ds_In = np.log(ds_ma)
    ds_In = ds_In.where(np.isinf(ds_In) == np.nan)  # = np.nan  #Change infinity to NaN
    #ds_In = ds_In.where(np.isinf(ds_In) == False)  # = np.nan  #Change infinity to NaN

    #ds_mu = ds_ma.mean(dimension)
    # Overall Mean of Moving Averages
    ds_mu = ds_ma.mean(dimension)

    # Summation of Natural log of moving averages
    ds_sum = ds_In.sum(dimension)

    # Computing essentials for gamma distribution
    n = ds_In[thresh - 1:, :, :].count(dimension)  # size of data
    A = np.log(ds_mu) - (ds_sum / n)  # Computing A
    alpha = (1 / (4 * A)) * (1 + (1 + ((4 * A) / 3)) ** 0.5)  # Computing alpha  (a)
    beta = ds_mu / alpha  # Computing beta (scale)

    # Gamma Distribution (CDF)
    gamma_func = lambda data, a, scale: st.gamma.cdf(data, a=a, scale=scale)
    gamma = xr.apply_ufunc(gamma_func, ds_ma, alpha, beta)

    # Standardized Precipitation Index (Inverse of CDF)
    norminv = lambda data: st.norm.ppf(data, loc=0, scale=1)
    norm_spi = xr.apply_ufunc(norminv, gamma)  # loc is mean and scale is standard dev.

    return ds_ma, ds_In, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi

# Variables
da_data = xr.open_dataset('.nc/ERA5Land_Monthly_01dd.nc')
ds_RR = da_data['tp']  # Precipitation var name
i = 3  # Index number
lim_north = 16
lim_south = -58
lim_east = -25
lim_west = -96
year_min = 2015
year_max = 2022
show_plot = True  # Verbose plot

# SPI calculation
ds_RR_ze = ds_RR.sel(longitude=slice(lim_west,lim_east), latitude=slice(lim_north, lim_south), time=slice(str(year_min), str(year_max)))
da_data['spi_'+str(i)] = spi(ds_RR_ze, i, 'time')[0]*1000
print('\n')
print(da_data)

# Plots
#for year in range(year_min+i-1,year_max+1):
for year in range(year_min,year_max+1):
    print('Plotting: %s' % year)
    # Plot Precipitation
    da_data_p = da_data
    da_data_p['tp'].sel(time=str(year)).plot(cmap='RdBu', col='time', col_wrap=4, vmin=0, vmax=0.01)
    plt.ylim(lim_south, lim_north)
    plt.xlim(lim_west,lim_east)
    if show_plot: plt.show()
    plt.close('all')
    # Plot SPI
    da_data_spi = da_data
    da_data_spi['spi_'+str(i)].sel(time=str(year)).plot(cmap='RdBu', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
    if show_plot: plt.show()
    plt.close('all')

# https://github.com/jeffjay88/Climate_Indices/blob/main/NC_spi_pandas.ipynb