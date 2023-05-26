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

    # Standardized Precipitation Index   (Inverse of CDF)
    norminv = lambda data: st.norm.ppf(data, loc=0, scale=1)
    norm_spi = xr.apply_ufunc(norminv, gamma)  # loc is mean and scale is standard dev.

    return ds_ma, ds_In, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi


# Variables
path = ''
nc_file = 'cru_ts4.03.1901.2018.pre.dat.nc'
times = [1, 3]  # SPI index #
feature_name = 'pre'
lim_north = 16
lim_south = -58
lim_east = -25
lim_west = -96
year_min = 2010
year_max = 2012
p_max_plot = 250  # Maximum value for plotting ramp
show_plot = False  # Verbose plot
save_spi_nc = True

# Procedure
da_data = xr.open_dataset(path+nc_file)
ds_RR = da_data[feature_name]
print(da_data)
p_plot = True  # Print precipitation control
for i in times:
    ds_RR_ze = ds_RR.sel(lon=slice(lim_west, lim_east), lat=slice(lim_south, lim_north),
                                 time=slice(str(year_min), str(year_max)))
    da_data['spi_' + str(i)] = spi(ds_RR_ze, i, 'time')[9]
    # Plot
    for year in range(year_min, year_max + 1):
        print('Processing SPI_%s_%s' % (str(i), str(year)))
        if p_plot:
            da_data[feature_name].sel(time=str(year)).plot(cmap='Blues', col='time', col_wrap=4, vmin=0, vmax=p_max_plot)
            plt.ylim(lim_south, lim_north)
            plt.xlim(lim_west, lim_east)
            plt.savefig('graph/' + 'P_' + str(year) + '.png')
            if show_plot: plt.show()
        da_data['spi_' + str(i)].sel(time=str(year)).plot(cmap='RdBu', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
        plt.ylim(lim_south, lim_north)
        plt.xlim(lim_west, lim_east)
        plt.savefig('graph/' + 'SPI_' + str(i) + '_' + str(year) + '.png')
        if show_plot: plt.show()
        plt.close('all')
    p_plot = False
print(da_data)
if save_spi_nc: da_data.to_netcdf('spi.nc')