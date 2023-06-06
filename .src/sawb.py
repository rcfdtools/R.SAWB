# SPI calculations for multiple data sources

# Import public libraries
import warnings
warnings.filterwarnings('ignore')
import glob
import os
import shutil
import pandas as pd
import numpy as np
import xarray as xr
from scipy import stats as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
from dbfread import DBF
import tabulate
import sawb_functions as sawbf
import sawb_dictionary as sawbd



# *****************************************************************************************
# General variables & directories
# *****************************************************************************************
ppoi_num = 1  # <<<<<<<< PPOI number to process
purge_ppoi_folder = True  # Delete all previous SPI results. Set False if you require run many .nc data sources
data_path = '../.nc/'
ppoi_path = '../.ppoi/'+str(ppoi_num)+'/'
if purge_ppoi_folder and os.path.exists(ppoi_path):  # Purge all previous results
    shutil.rmtree(ppoi_path+'spi')
    os.mkdir(ppoi_path + 'spi')
    os.mkdir(ppoi_path+'spi/cru')
    os.mkdir(ppoi_path+'spi/era5')
if not os.path.exists(ppoi_path):  # Create folder structure if not exists
    os.mkdir(ppoi_path)
    os.mkdir(ppoi_path+'awb')
    os.mkdir(ppoi_path+'awb/basin')
    os.mkdir(ppoi_path+'awb/fdr')
    os.mkdir(ppoi_path+'awb/graph')
    os.mkdir(ppoi_path+'awb/pflow')
    os.mkdir(ppoi_path+'awb/qm')
    os.mkdir(ppoi_path+'awb/shpin')
    os.mkdir(ppoi_path+'awb/shpout')
    os.mkdir(ppoi_path+'awb/shpout/basin')
    os.mkdir(ppoi_path+'awb/shpout/basindissolve')
    os.mkdir(ppoi_path+'awb/shpout/watershed')
    os.mkdir(ppoi_path+'awb/watershed')
    os.mkdir(ppoi_path+'awb/winddir')
    os.mkdir(ppoi_path+'swb')
    os.mkdir(ppoi_path+'spi')
    os.mkdir(ppoi_path+'spi/cru')
    os.mkdir(ppoi_path+'spi/era5')
    shutil.copyfile('../.ppoi/1/ppoi.py', ppoi_path+'ppoi.py')  # PPOI #1 contains the template parameters
sys.path.insert(0,ppoi_path)  # PPOI path insert and parameters to process
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
spi_colors = ['#FF0000', '#FFAA00', '#FFFF00', '#C8C8C8', '#E9CCF9', '#833393', '#0000FF']
# AWB parameters
awb_qm_join_file = 'awb_qm.csv' # Joined file name
awb_qm_pivot_file = 'awb_qm_pivot.csv' # Joined average flow file name
awb_aa_pivot_file = 'awb_aa_pivot.csv' # Joined accumulation area file name
awb_eval = ppoi.awb_eval
file_log_name = ppoi_path + data_source[data_source_num] + '_readme.md'  # Markdown file log
file_log = open(file_log_name, 'w+')   # w+ create the file if it doesn't exist

# *****************************************************************************************
# Preliminar details & parameters
# *****************************************************************************************
if year_min > year_max:
    year_min_aux = year_max
    year_max = year_min
    year_min = year_min_aux
sawbf.print_log(file_log, '# %s\nKeywords: %s\n\n%s' %(ppoi.sawb_title, sawbd.sawb_keywords, ppoi.sawb_desc))
sawbf.print_log(file_log, '\n\n## General parameters  ' +
                '\n\n<div align="center">' +
                '\n\n| Parameter | Description |' +
                '\n|:---|:---|' +
                '\n| PPOI | %d |' %ppoi_num +
                '\n| Client | %s |' %ppoi.sawb_client +
                '\n| Order | %s |' %ppoi.sawb_order +
                '\n| Date | %s |' %ppoi.sawb_date +
                '\n| Dataset | %s |' %nc_file +
                '\n| Units conversion multiplier | %f |' %units_mult +
                '\n| Precipitation maximum plot value | %f |' %ppoi.p_max_plot +
                '\n| Year from | %d |' %year_min +
                '\n| Year to | %d |' %year_max +
                '\n\n</div>\n'
                )
sawbf.print_log(file_log, '\n' + sawbd.p_max_plot_desc)

# *****************************************************************************************
# Standardized Precipitation Index (SPI) - Procedure
# *****************************************************************************************
if polygon_eval or point_eval:
    sawbf.print_log(file_log, '\n\n## Standardized Precipitation Index (SPI)\n\n' +
                    sawbd.spi_desc +
                    '\n\n%s' %sawbd.precipitation_desc +
                    '\n\nSPI index mobile average times: %s' %ppoi.times)
# SPI - Polygon processing
if polygon_eval:
    sawbf.print_log(file_log, '\n\n### Processing polygon over N: %f°, S: %f°, E: %f°, W: %f°\n\n' % (lim_north, lim_south, lim_east, lim_west))
    da_data = xr.open_dataset(data_path+nc_file)
    da_data[feature_name[data_source_num]] = da_data[feature_name[data_source_num]] * units_mult
    ds_rr = da_data[feature_name[data_source_num]]
    year_min = sawbf.year_range_eval(da_data['time'], year_min, year_max)[0]
    year_max = sawbf.year_range_eval(da_data['time'], year_min, year_max)[1]
    print('\nNetCDF contents\n',da_data,'\n')
    p_plot = True  # Control the precipitation plot
    records = 0
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
        da_data['spi_' + str(i)] = sawbf.spi(ds_rr_ze, i, 'time')[9]
        for year in range(year_min, year_max + 1):
            da_count = da_data[feature_name[data_source_num]].sel(time=str(year)).count()
            print('Processing %s_spi_%s_%s (%d records)' % (data_source[data_source_num], str(i), str(year), da_count))
            records += da_count
            if da_count:
                # Plotting feature yearly maps
                if p_plot:
                    #sawbf.print_log(file_log, '\n%d precipitation map (%d records)\n' %(year, da_count), center_div=False)
                    p = da_data[feature_name[data_source_num]].sel(time=str(year)).plot(cmap='YlGnBu', col='time', col_wrap=4, vmin=0, vmax=p_max_plot)
                    da_count = da_data['spi_' + str(i)].count()
                    plt.ylim(lim_south, lim_north)
                    plt.xlim(lim_west, lim_east)
                    p_fig = 'spi/'+data_source[data_source_num]+'/'+data_source[data_source_num]+'_p_'+str(year)+'.png'
                    plt.savefig(ppoi_path+p_fig, dpi=dpi)
                    if show_plot: plt.show()
                    sawbf.print_log(file_log, '[`P-%d`](%s) ' %(year, p_fig))
                # Plotting feature SPI maps
                #sawbf.print_log(file_log, '%d SPI-%s map' %(year, i), center_div=False)
                da_data['spi_' + str(i)].sel(time=str(year)).plot(col='time', col_wrap=4, vmin=-2.5, vmax=2.5, levels=[-2, -1.5, -1, 1, 1.5, 2], colors=spi_colors)
                spi_fig = 'spi/'+data_source[data_source_num]+'/'+data_source[data_source_num]+'_spi_'+str(i)+'_'+str(year)+'.png'
                plt.ylim(lim_south, lim_north)
                plt.xlim(lim_west, lim_east)
                plt.savefig(ppoi_path+spi_fig, dpi=dpi)
                if show_plot: plt.show()
                plt.close('all')
                sawbf.print_log(file_log, '[`SPI-%d-%d`](%s) ' %(i,year,spi_fig))
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
    # Gif animations
    if __name__ == '__main__':
        sawbf.print_log(file_log, '\n\nPrecipitation')
        p_gif = 'spi/'+data_source[data_source_num]+'/'
        key_name = data_source[data_source_num]+'_p'
        sawbf.make_gif(ppoi_path+p_gif, key_name, '.png')
        sawbf.print_log(file_log, '\n![R.SAWB](%s)' %(p_gif+key_name+'.gif'))
        for i in times:
            print('\nCreating %s_spi_%d.gif' %(data_source[data_source_num], i))
            sawbf.print_log(file_log, '\nSPI-%d' % i)
            spi_gif = 'spi/' + data_source[data_source_num] + '/'
            key_name = data_source[data_source_num] + '_spi_' + str(i)
            sawbf.make_gif(ppoi_path+spi_gif, key_name, '.png')
            sawbf.print_log(file_log, '\n\n![R.SAWB](%s)' %(spi_gif+key_name+'.gif'))
    sawbf.print_log(file_log, '\n\nRecords processed: %d' %records)
# SPI - Point processing
if point_eval:
    print('\nProcessing point in Latitude: %f°, Longitude: %f° for nearest' %(point_latitude, point_longitude))
    # Extract values from NetCDF
    da_data = xr.open_dataset(data_path + nc_file)
    da_data[feature_name[data_source_num]] = da_data[feature_name[data_source_num]] * units_mult
    ds_rr = da_data[feature_name[data_source_num]]
    year_min = sawbf.year_range_eval(da_data['time'], year_min, year_max)[0]
    year_max = sawbf.year_range_eval(da_data['time'], year_min, year_max)[1]
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
        x = sawbf.spi_point(data[feature_name[data_source_num]], i)
        data['spi_' + str(i)] = x[9]
    print('\nDataframe with SPI calculations\n', data)
    data.to_csv(ppoi_path+'spi/'+data_source[data_source_num]+'_spi_point.csv', encoding='utf-8', index=True)
    # Plot SPI data
    fig, axes = plt.subplots(nrows=len(times), figsize=(10, 8))
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


# *****************************************************************************************
# AWB - Post-processing procedure (ArcGIS for Desktop SAWB.tbx need to be run before)
# *****************************************************************************************
if awb_eval:
    print('\nPost-processing Atmospheric Water Balance - AWB\n')
    awb_dbf_files = glob.glob(ppoi_path + 'awb/qm/' + '*.dbf')
    awb_df = pd.DataFrame()
    for i in awb_dbf_files:
        print('AWB - Processing: %s' %i)
        awb_dbf = DBF(i)
        awb_data_result = pd.DataFrame(iter(awb_dbf))
        awb_df = pd.concat([awb_df, awb_data_result], ignore_index=False)
    awb_year_min = awb_df['year'].min()
    awb_year_max = awb_df['year'].max()
    year_list = np.linspace(awb_year_min, awb_year_max, (awb_year_max-awb_year_min+1))
    print('\nYears found: %s' %year_list)
    awb_df['date'] = pd.to_datetime(awb_df['date'])
    awb_df.sort_values(by='date', inplace=True)
    print('\nDataframe types\n', awb_df.dtypes)
    awb_df = awb_df.set_index('date')
    print('\nDataframe sample\n', awb_df)
    awb_df.to_csv(ppoi_path+'awb/'+awb_qm_join_file, encoding='utf-8', index=True)
    awb_df.plot(y='SUM', figsize=(10,6), title='AWB - Atmospheric monthly average flow serie', ylabel='Qm, m³/s')
    plt.savefig(ppoi_path+'awb/graph/awb_qm_serie.png')
    if show_plot: plt.show()
    awb_df.plot(y='Akm2', figsize=(10,6), title='AWB - Atmospheric monthly accumulation area serie', ylabel='A, km²')
    plt.savefig(ppoi_path+'awb/graph/awb_aa_serie.png')
    if show_plot: plt.show()
    pivot_table_qm = awb_df.pivot_table(index='month', columns='year', values='SUM')
    print('\nQm (m³/s) pivot table sample\n', pivot_table_qm)
    pivot_table_qm.to_csv(ppoi_path+'awb/'+awb_qm_pivot_file, encoding='utf-8', index=True)
    pivot_table_qm.plot(y=year_list, figsize=(10,6), title='AWB - Atmospheric monthly average flow by year', ylabel='Qm, m³/s')
    plt.savefig(ppoi_path+'awb/graph/awb_qm_monthly.png')
    if show_plot: plt.show()
    pivot_table_aa = awb_df.pivot_table(index='month', columns='year', values='Akm2')
    print('\nAa (km²) pivot table sample\n', pivot_table_aa)
    pivot_table_aa.to_csv(ppoi_path+'awb/'+awb_aa_pivot_file, encoding='utf-8', index=True)
    pivot_table_aa.plot(y=year_list, figsize=(10,6), title='AWB - Atmospheric monthly accumulation area by year', ylabel='A, km²')
    #plt.xticks(range(len(pivot_table_aa)),labels=range(0, len(pivot_table_aa)))
    plt.savefig(ppoi_path+'awb/graph/awb_aa_monthly.png')
    if show_plot: plt.show()
    plt.close('all')
