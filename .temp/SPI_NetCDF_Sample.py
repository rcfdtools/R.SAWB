import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import xarray as xr
import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plt

# Standardized Precipitation Index Function
def spi(ds, thresh, dimension):
    # ds - data ; thresh - time interval / scale; dimension - dimension as a string

    # Rolling Mean / Moving Averages
    ds_ma = ds.rolling(time=thresh, center=False).mean(dim=dimension)

    # Natural log of moving averages
    ds_In = np.log(ds_ma)
    ds_In = ds_In.where(np.isinf(ds_In) == False)  # = np.nan  #Change infinity to NaN

    ds_mu = ds_ma.mean(dimension)

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

    # Standardized Precipitation Index   (Inverse of CDF)
    norminv = lambda data: st.norm.ppf(data, loc=0, scale=1)
    norm_spi = xr.apply_ufunc(norminv, gamma)  # loc is mean and scale is standard dev.

    return ds_ma, ds_In, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi

# Variables
da_data = xr.open_dataset('cru_ts4.03.1901.2018.pre.dat.nc')
ds_RR = da_data['pre']
times = [1, 3, 6, 9, 12, 24]  # SPI index #
lim_north = 16
lim_south = -58
lim_east = -25
lim_west = -96
year_min = 1980
year_max = 2018
show_plot = False  # Verbose plot

# Procedure
for i in times:
    ds_RR_WestAfrica = ds_RR.sel(lon=slice(lim_west,lim_east), lat=slice(lim_south, lim_north),time=slice(str(year_min), str(year_max)))
    da_data['spi_'+str(i)] = spi(ds_RR_WestAfrica,i,'time')[9]
    # Plot
    for year in range(year_min, year_max + 1):
        print('Processing SPI_%s_%s' %(str(i), str(year)))
        da_data['spi_'+str(i)].sel(time=str(year)).plot(cmap='RdBu', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
        plt.ylim(lim_south, lim_north)
        plt.xlim(lim_west, lim_east)
        plt.savefig('graph/'+'SPI_'+str(i)+'_'+str(year)+'.png')
        if show_plot: plt.show()
        plt.close('all')
print(da_data)

