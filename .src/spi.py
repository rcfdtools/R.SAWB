# SPI calculations for multiple data sources

# Import public libraries
import warnings
warnings.filterwarnings('ignore')
import os
import shutil
import pandas as pd
import numpy as np
import xarray as xr
from scipy import stats as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys


# Standardized Precipitation Index Function - Polygon with .nc
def spi(ds, thresh, dimension):
    # Original function script from https://github.com/jeffjay88/Climate_Indices
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

# Standardized Precipitation Index Function - Point with .csv
def spi_point(ds, thresh):
    # ds - data ; thresh - time interval / scale

    # Rolling Mean / Moving Averages
    ds_ma = ds.rolling(thresh, center=False).mean()

    # Natural log of moving averages
    ds_In = np.log(ds_ma)
    ds_In[np.isinf(ds_In) == True] = np.nan  # Change infinity to NaN

    # Overall Mean of Moving Averages
    ds_mu = np.nanmean(ds_ma)

    # Summation of Natural log of moving averages
    ds_sum = np.nansum(ds_In)

    # Computing essentials for gamma distribution
    n = len(ds_In[thresh - 1:])  # size of data
    A = np.log(ds_mu) - (ds_sum / n)  # Computing A
    alpha = (1 / (4 * A)) * (1 + (1 + ((4 * A) / 3)) ** 0.5)  # Computing alpha  (a)
    beta = ds_mu / alpha  # Computing beta (scale)

    # Gamma Distribution (CDF)
    gamma = st.gamma.cdf(ds_ma, a=alpha, scale=beta)

    # Standardized Precipitation Index   (Inverse of CDF)
    norm_spi = st.norm.ppf(gamma, loc=0, scale=1)  # loc is mean and scale is standard dev.

    return ds_ma, ds_In, ds_mu, ds_sum, n, A, alpha, beta, gamma, norm_spi

def year_range_eval(data_time, year_min, year_max):
    year_min_data = data_time.min().values
    year_min_data = pd.to_datetime(year_min_data).year
    year_max_data = data_time.max().values
    year_max_data = pd.to_datetime(year_max_data).year
    if year_min_data > year_min:
        print('\nAttention: your enter minimum year value %d has changed for %d' %(year_min, year_min_data))
        year_min = year_min_data
    if year_max_data < year_max:
        print('Attention: your enter maximum year value %d has changed for %d' %(year_max, year_max_data))
        year_max = year_max_data
    return year_min, year_max

# Variables & directories
ppoi_num = 2  # <<<<<<<< ppoi number to process
data_path = '../.nc/'
ppoi_path = '../.ppoi/'+str(ppoi_num)+'/'
purge_ppoi_folder = True  # Delete all previous results. Set False if you require run many .nc data sources
if purge_ppoi_folder and os.path.exists(ppoi_path):  # Purge all previous results
    shutil.rmtree(ppoi_path+'spi')
    os.mkdir(ppoi_path + 'spi')
    os.mkdir(ppoi_path+'spi/cru')
    os.mkdir(ppoi_path+'spi/era5')
if not os.path.exists(ppoi_path):  # Create folder structure if not exists
    os.mkdir(ppoi_path)
    os.mkdir(ppoi_path+'basin')
    os.mkdir(ppoi_path+'fdr')
    os.mkdir(ppoi_path+'graph')
    os.mkdir(ppoi_path+'pflow')
    os.mkdir(ppoi_path+'qm')
    os.mkdir(ppoi_path+'shpin')
    os.mkdir(ppoi_path+'shpout')
    os.mkdir(ppoi_path+'shpout/basin')
    os.mkdir(ppoi_path+'shpout/basindissolve')
    os.mkdir(ppoi_path+'shpout/watershed')
    os.mkdir(ppoi_path+'spi')
    os.mkdir(ppoi_path+'spi/cru')
    os.mkdir(ppoi_path+'spi/era5')
    os.mkdir(ppoi_path+'watershed')
    os.mkdir(ppoi_path+'winddir')
    shutil.copyfile('../.ppoi/1/ppoi.py', ppoi_path+'ppoi.py')  # PPOI #1 contains the parameters template
sys.path.insert(0,ppoi_path)  # PPOI path insert
import ppoi
nc_file = ppoi.nc_file
p_max_plot = ppoi.p_max_plot
data_source_num = ppoi.data_source_num
data_source = ['cru', 'era5']
feature_name = ['pre', 'tp']
times = ppoi.times
lim_north = ppoi.lim_north
lim_south = ppoi.lim_south
lim_east = ppoi.lim_east
lim_west = ppoi.lim_west
point_latitude = ppoi.point_latitude
point_longitude = ppoi.point_longitude
year_min = ppoi.year_min
year_max = ppoi.year_max
units_mult = ppoi.units_mult
polygon_eval = ppoi.polygon_eval
point_eval = ppoi.point_eval
dpi = 128  # Save plot resolution
show_plot = False  # Verbose plot
save_spi_nc = True  # Export .nc with SPI values
plt_title = 'https://github.com/rcfdtools/R.SAWB'
spi_colors = ['#FF0000', '#FFAA00', '#FFFF00', '#F0F0F0', '#E9CCF9', '#833393', '#0000FF']


# Procedure
print('Processing PPOI: %s' %ppoi_path,
      '\nData file: %s' %nc_file,
      '\nUnits conversion multiplier: %f' %units_mult)
# SPI - Polygon processing
if polygon_eval:
    print('\nProcessing polygon over N: %f°, S: %f°, E: %f°, W: %f°' % (lim_north, lim_south, lim_east, lim_west))
    da_data = xr.open_dataset(data_path+nc_file)
    da_data[feature_name[data_source_num]] = da_data[feature_name[data_source_num]] * units_mult
    ds_rr = da_data[feature_name[data_source_num]]
    year_min = year_range_eval(da_data['time'], year_min, year_max)[0]
    year_max = year_range_eval(da_data['time'], year_min, year_max)[1]
    print('\nNetCDF contents\n',da_data,'\n')
    p_plot = True  # Control the precipitation plot
    for i in times:
        match data_source_num:
            case 0:  # CRU data
                ds_rr_ze = ds_rr.sel(lon=slice(lim_west, lim_east), lat=slice(lim_south, lim_north),
                                         time=slice(str(year_min), str(year_max)))
            case 1:  # ERA5 reanalysis
                ds_rr_ze = ds_rr.sel(longitude=slice(lim_west, lim_east), latitude=slice(lim_north, lim_south),
                             time=slice(str(year_min), str(year_max)))
            case _:
                print('\nAttention: datasource %s doesn''t exist or nor defined' %data_source_num)
        # Plot
        da_data['spi_' + str(i)] = spi(ds_rr_ze, i, 'time')[9]
        for year in range(year_min, year_max + 1):
            da_count = da_data[feature_name[data_source_num]].sel(time=str(year)).count()
            print('Processing SPI_%s_%s (%d records)' % (str(i), str(year), da_count))
            if da_count:
                # Plotting feature yearly maps
                if p_plot:
                    p = da_data[feature_name[data_source_num]].sel(time=str(year)).plot(cmap='YlGnBu', col='time', col_wrap=4, vmin=0, vmax=p_max_plot)
                    da_count = da_data['spi_' + str(i)].count()
                    plt.ylim(lim_south, lim_north)
                    plt.xlim(lim_west, lim_east)
                    plt.savefig(ppoi_path+'spi/'+data_source[data_source_num]+'/'+data_source[data_source_num]+'_p_'+str(year)+'.png', dpi=dpi)

                    if show_plot: plt.show()
                # Plotting feature SPI maps
                da_data['spi_' + str(i)].sel(time=str(year)).plot(col='time', col_wrap=4, vmin=-2.5, vmax=2.5, levels=[-2, -1.5, -1, 1, 1.5, 2], colors=spi_colors)
                plt.ylim(lim_south, lim_north)
                plt.xlim(lim_west, lim_east)
                plt.savefig(ppoi_path+'spi/'+data_source[data_source_num]+'/'+data_source[data_source_num]+'_spi_'+str(i)+'_'+str(year)+'.png', dpi=dpi)
                if show_plot: plt.show()
                plt.close('all')
        p_plot = False
    # Export .nc with SPI calculations over ZE as .csv
    match data_source_num:
        case 0:  # CRU data
            da_data = da_data.sel(lon=slice(lim_west, lim_east), lat=slice(lim_south, lim_north),
                                  time=slice(str(year_min), str(year_max)))
        case 1:  # ERA5 reanalysis
            da_data = da_data.sel(longitude=slice(lim_west, lim_east), latitude=slice(lim_north, lim_south),
                             time=slice(str(year_min), str(year_max)))
        case _:
            print('\nAttention: datasource %s doesn''t exist or nor defined' %data_source_num)
    df = da_data.to_dataframe()
    print('Exporting %s_polygon_spi.csv' %data_source[data_source_num])
    df.to_csv(ppoi_path+'spi/'+str(data_source[data_source_num])+'_spi_polygon.csv', encoding='utf-8', index=True)
    print(da_data)
    # Export .nc with SPI calculations over ZE as .nc
    if save_spi_nc:
        print('Exporting %s_polygon.nc' %data_source[data_source_num])
        da_data.to_netcdf(ppoi_path+'spi/'+data_source[data_source_num]+'_spi_polygon.nc')

# SPI - Point processing
if point_eval:
    print('\nProcessing point in Latitude: %f°, Longitude: %f° for nearest' %(point_latitude, point_longitude))
    # Extract values from NetCDF
    da_data = xr.open_dataset(data_path + nc_file)
    da_data[feature_name[data_source_num]] = da_data[feature_name[data_source_num]] * units_mult
    ds_rr = da_data[feature_name[data_source_num]]
    year_min = year_range_eval(da_data['time'], year_min, year_max)[0]
    year_max = year_range_eval(da_data['time'], year_min, year_max)[1]
    match data_source_num:
        case 0:  # CRU data
            ds_rr_slice = ds_rr.sel(time=slice(str(year_min), str(year_max)))
            ds_rr_select = ds_rr_slice.sel(lon=point_longitude, lat=point_latitude, method='nearest')
        case 1:  # ERA5 reanalysis
            ds_rr_slice = ds_rr.sel(time=slice(str(year_min), str(year_max)))
            ds_rr_select = ds_rr_slice.sel(longitude=point_longitude, latitude=point_latitude, method='nearest')
        case _:
            print('\nAttention: datasource %s doesn''t exist or nor defined' % data_source_num)
    ds_rr_select.plot(figsize=(10, 7))
    plt.savefig(ppoi_path+'spi/'+data_source[data_source_num]+'_p_point.png', dpi=dpi)
    if show_plot: plt.show()
    df = ds_rr_select.to_dataframe()
    print('\nInitial dataframe\n', df)
    point_csv_file = ppoi_path+'spi/'+data_source[data_source_num]+'_p_point.csv'
    df.to_csv(point_csv_file, encoding='utf-8', index=True)
    # SPI calculation
    data = pd.read_csv(point_csv_file)
    data['time'] = pd.to_datetime(data['time'])
    print(data.dtypes)
    data = data.set_index('time')
    print(data.dtypes)
    for i in times:
        x = spi_point(data[feature_name[data_source_num]], i)
        data['spi_' + str(i)] = x[9]
    print('\nDataframe with SPI calculations\n', data)
    data.to_csv(ppoi_path+'spi/'+data_source[data_source_num]+'_spi_point.csv', encoding='utf-8', index=True)
    # Plot SPI data
    fig, axes = plt.subplots(nrows=len(times), figsize=(10, 7))
    plt.subplots_adjust(hspace=0.15)
    for i, ax in enumerate(axes):
        col_scheme = np.where(data['spi_' + str(times[i])] > 0, 'b', 'r')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.bar(data.index, data['spi_' + str(times[i])], width=25, align='center', color=col_scheme, label='SPI ' + str(times[i]))
        ax.axhline(y=0, color='k')
        ax.xaxis.set_major_locator(mdates.YearLocator(2))
        ax.legend(loc='upper right')
        ax.set_yticks(range(-3, 4), range(-3, 4))
        ax.set_ylabel('SPI', fontsize=12)
        if i < len(times) - 1:
            ax.set_xticks([], [])
        plt.xticks(rotation=90)
        #plt.title(plt_title)
    plt.savefig(ppoi_path + 'spi/' + data_source[data_source_num] + '_spi_point.png', dpi=dpi)
    if show_plot: plt.show()
    plt.close('all')
