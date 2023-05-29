# For multiple sources

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import xarray as xr
import numpy as np
from scipy import stats as st
import matplotlib.pyplot as plt
import datetime


# Standardized Precipitation Index Function
def spi(ds, thresh, dimension):
    # Original script from https://github.com/jeffjay88/Climate_Indices
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
path = '../.nc/'
nc_file = 'cru_ts4.03.1901.2018.pre.dat.nc'
nc_file = 'ERA5Land_Monthly_01dd.nc'
#p_max_plot = 500  # Maximum value for plotting ramp - cru data in milimeters
p_max_plot = 0.02  # Maximum value for plotting ramp - era5 data in meters
data_source_num = 1  # 0:cru, 1:era5...
data_source = ['cru', 'era5']
feature_name = ['pre', 'tp']
times = [1, 3, 6, 9, 12]  # SPI index #
lim_north = 5.735
lim_south = 3.625
lim_east = -72.875
lim_west = -74.875
year_min = 1970
year_max = 2030
dpi = 128  # Save plot resolution
show_plot = False  # Verbose plot
save_spi_nc = True  # Export .nc with SPI values
plt_title = 'https://github.com/rcfdtools/R.SAWB'
spi_colors = ['#FF0000', '#FFAA00', '#FFFF00', '#F0F0F0', '#E9CCF9', '#833393', '#0000FF']

# Procedure
da_data = xr.open_dataset(path+nc_file)
ds_RR = da_data[feature_name[data_source_num]]
year_min_data = da_data['time'].min().values
year_min_data = pd.to_datetime(year_min_data).year
year_max_data = da_data['time'].max().values
year_max_data = pd.to_datetime(year_max_data).year
if year_min_data > year_min:
    print('Attention: your enter minimum year value %d has to be change for %d' %(year_min, year_min_data))
    year_min = year_min_data
if year_max_data < year_max:
    print('Attention: your enter maximum year value %d has to be change for %d' %(year_max, year_max_data))
    year_max = year_max_data
print(da_data)
p_plot = True  # Print precipitation control
for i in times:
    match data_source_num:
        case 0:  # CRU data
            ds_RR_ze = ds_RR.sel(lon=slice(lim_west, lim_east), lat=slice(lim_south, lim_north),
                                     time=slice(str(year_min), str(year_max)))
        case 1:  # ERA-5 reanalysis
            ds_RR_ze = ds_RR.sel(longitude=slice(lim_west, lim_east), latitude=slice(lim_north, lim_south),
                         time=slice(str(year_min), str(year_max)))
        case _:
            print('Atention: datasource %s doesn''t exist or nor defined' %data_source_num)
    # Plot
    da_data['spi_' + str(i)] = spi(ds_RR_ze, i, 'time')[9]
    for year in range(year_min, year_max + 1):
        da_count = da_data[feature_name[data_source_num]].sel(time=str(year)).count()
        print('Processing SPI_%s_%s (%d records)' % (str(i), str(year), da_count))
        if da_count:
            # Plotting feature yearly maps
            if p_plot:
                da_data[feature_name[data_source_num]].sel(time=str(year)).plot(cmap='YlGnBu', col='time', col_wrap=4, vmin=0, vmax=p_max_plot)
                da_count = da_data['spi_' + str(i)].count()
                plt.ylim(lim_south, lim_north)
                plt.xlim(lim_west, lim_east)
                plt.savefig('../.spi/graph/'+data_source[data_source_num]+'/'+data_source[data_source_num]+'_p_'+str(year)+'.png', dpi=dpi)
                if show_plot: plt.show()
            # Plotting feature SPI maps
            da_data['spi_' + str(i)].sel(time=str(year)).plot(col='time', col_wrap=4, vmin=-2.5, vmax=2.5, levels=[-2, -1.5, -1, 1, 1.5, 2], colors=spi_colors)
            plt.ylim(lim_south, lim_north)
            plt.xlim(lim_west, lim_east)
            plt.savefig('../.spi/graph/'+data_source[data_source_num]+'/'+data_source[data_source_num]+'_spi_'+str(i)+'_'+str(year)+'.png', dpi=dpi)
            if show_plot: plt.show()
            plt.close('all')
    p_plot = False
# Export .nc with SPI calculations over ZE as .csv
match data_source_num:
    case 0:  # CRU data
        da_data = da_data.sel(lon=slice(lim_west, lim_east), lat=slice(lim_south, lim_north),
                              time=slice(str(year_min), str(year_max)))
    case 1:  # ERA-5 reanalysis
        da_data = da_data.sel(longitude=slice(lim_west, lim_east), latitude=slice(lim_north, lim_south),
                         time=slice(str(year_min), str(year_max)))
    case _:
        print('Atention: datasource %s doesn''t exist or nor defined' %data_source_num)
df = da_data.to_dataframe()
print('Exporting %s_ze.csv' %data_source[data_source_num])
df.to_csv('../.spi/'+str(data_source[data_source_num])+'_ze.csv', encoding='utf-8', index=True)
print(da_data)
# Export .nc with SPI calculations over ZE as .nc
if save_spi_nc:
    print('Exporting %s_ze.nc' %data_source[data_source_num])
    da_data.to_netcdf('../.spi/'+data_source[data_source_num]+'_ze.nc')

# plt.title(plt_title)