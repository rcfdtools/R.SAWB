# SPI for ERA-5 reanalysis data

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

    # Standardized Precipitation Index   (Inverse of CDF)
    norminv = lambda data: st.norm.ppf(data, loc=0, scale=1)
    norm_spi = xr.apply_ufunc(norminv, gamma)  # loc is mean and scale is standard dev.

    return ds_ma, ds_In, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi

def spi_test(ds, thresh, dimension):
    # ds - data ; thresh - time interval / scale; dimension - dimension as a string

    # Rolling Mean / Moving Averages
    ds_ma = ds.rolling(time=thresh, center=False).mean(dim=dimension)

    # Rolling Standard deviation / Moving Averages
    ds_std = ds.rolling(time=thresh, center=False).std(dim=dimension)

    # Overall Mean of Moving Averages
    ds_mu = ds_ma.mean(dimension)

    # Overall Mean of Standard deviation
    ds_stdm = ds_std.mean(dimension)

    ds_spi = (ds - ds_mu) / ds_stdm

    return ds_spi


# Variables
path = '../.nc/'
nc_file = 'ERA5Land_Monthly_01dd.nc'
times = [1, 3]  # SPI index #
feature_name = 'tp'
lim_north = 5.735
lim_south = 3.625
lim_east = -72.875
lim_west = -74.875
year_min = 2010
year_max = 2012
dpi = 128  # Save plot resolution
p_max_plot = 10  # Maximum value for plotting ramp
show_plot = False  # Verbose plot
save_spi_nc = False  # Create a .nc file with the new features

# Procedure
da_data = xr.open_dataset(path+nc_file)
da_data['tp_mm'] = da_data[feature_name] * 1000  # ERA-5 Convert meters to millimeters
ds_RR = da_data['tp_mm']
print(da_data)
p_plot = True  # Print precipitation control
for i in times:
    ds_RR_ze = ds_RR.sel(longitude=slice(lim_west, lim_east), latitude=slice(lim_north, lim_south),
                                 time=slice(str(year_min), str(year_max)))
    da_data['spi_' + str(i)] = spi(ds_RR_ze, i, 'time')[9]
    #da_data['spi_' + str(i)] = spi(ds_RR_ze, i, 'time')[0]
    # Plot
    for year in range(year_min, year_max + 1):
        print('Processing SPI_%s_%s' % (str(i), str(year)))
        if p_plot:
            da_data['tp_mm'].sel(time=str(year)).plot(cmap='YlGnBu', col='time', col_wrap=4, vmin=0, vmax=p_max_plot)
            plt.ylim(lim_south, lim_north)
            plt.xlim(lim_west, lim_east)
            plt.savefig('../.spi/graph/era5/' + 'P_' + str(year) + '.png', dpi=dpi)
            if show_plot: plt.show()
        da_data['spi_' + str(i)].sel(time=str(year)).plot(cmap='twilight_shifted', col='time', col_wrap=4, vmin=-2.5, vmax=2.5)
        plt.ylim(lim_south, lim_north)
        plt.xlim(lim_west, lim_east)
        plt.savefig('../.spi/graph/era5/' + 'SPI_' + str(i) + '_' + str(year) + '.png', dpi=dpi)
        if show_plot: plt.show()
        plt.close('all')
    p_plot = False
print(da_data)
if save_spi_nc:
    print('Exporting spi.nc')
    da_data.to_netcdf('.spi/spi.nc')
