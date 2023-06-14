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
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
import sawb_functions as sawbf
import sawb_dictionary as sawbd



# *****************************************************************************************
# General variables & directories
# *****************************************************************************************
ppoi_num = 1  # <<<<<<<< PPOI number to process
purge_ppoi_folder = False  # Delete all previous SPI results. Set False if you require run many .nc data sources
data_path = '../.netcdf/'
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
    os.mkdir(ppoi_path+'awb/qpot')
    os.mkdir(ppoi_path+'awb/q')
    os.mkdir(ppoi_path+'awb/shpin')
    os.mkdir(ppoi_path+'awb/shpout')
    os.mkdir(ppoi_path+'awb/shpout/basin')
    os.mkdir(ppoi_path+'awb/shpout/basindissolve')
    os.mkdir(ppoi_path+'awb/shpout/watershed')
    os.mkdir(ppoi_path+'awb/watershed')
    os.mkdir(ppoi_path+'awb/winddir')
    os.mkdir(ppoi_path+'graph')
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
meridians_sep = ppoi.meridians_sep
dpi = 128  # Save plot resolution
show_plot = False  # Verbose plot
save_spi_nc = True  # Export .nc with SPI values
plt_title = 'https://github.com/rcfdtools/R.SAWB'
spi_colors = ['#FF0000', '#FFAA00', '#FFFF00', '#C8C8C8', '#E9CCF9', '#833393', '#0000FF']
# AWB parameters
awb_q_join_file = 'awb_q.csv' # Joined file name
awb_q_pivot_file = 'awb_q_pivot.csv' # Joined average flow file name
awb_a_pivot_file = 'awb_a_pivot.csv' # Joined accumulation area file name
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
                '\n| Dataset | [%s](%s) |' % (nc_file, '../../.netcdf/') +
                '\n| Units conversion multiplier | %f |' %units_mult +
                '\n| Precipitation maximum plot value | %f |' %ppoi.p_max_plot +
                '\n| Year from | %d |' %year_min +
                '\n| Year to | %d |' %year_max +
                '\n\n</div>\n'
                )
sawbf.print_log(file_log, '\n%s \n\n' %sawbd.p_max_plot_desc)

# *****************************************************************************************
# General map locations
# *****************************************************************************************
projection = ['ortho', 'lcc']
for i in projection:
    if i == 'ortho':
        fig = plt.figure(figsize=(4, 4))
        title = 'Global location'
        map_file = 'global_map.png'
        meridians_sep = meridians_sep * 2
    else:
        fig = plt.figure(figsize=(4, 4))
        title = 'Regional location'
        map_file = 'regional_map.png'
        meridians_sep = meridians_sep
    map = Basemap(projection=i, lat_0=point_latitude, lon_0=point_longitude, resolution='l', width=5E6, height=4E6)
    map.drawcountries(linewidth=0.25)
    map.drawcoastlines(linewidth=0.35)
    map.fillcontinents(color='coral', lake_color='aqua', alpha=1)
    map.drawmapboundary(fill_color='aqua')
    map.drawmeridians(np.arange(0,360,meridians_sep))
    map.drawparallels(np.arange(-90,90,meridians_sep))
    x, y = map(point_longitude, point_latitude)
    plt.plot(x, y, 'ok', markersize=3)
    plt.text(x, y, ' PPOI (Lat: %s, Lon: %s)' %(point_latitude, point_longitude), fontsize=10);
    plt.title(title)
    parallels = np.arange(0., 81, meridians_sep)
    map.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(10., 351., meridians_sep)
    map.drawmeridians(meridians, labels=[True, False, False, True], rotation=45)
    if show_plot: plt.show()
    map_fig = ''
    plt.savefig(ppoi_path + 'graph/' + map_file, dpi=dpi)
    plt.close()
    sawbf.print_log(file_log, '![R.SAWB](graph/%s)' % map_file, center_div=False)

# *****************************************************************************************
# Standardized Precipitation Index (SPI) - Procedure
# *****************************************************************************************
if polygon_eval or point_eval:
    sawbf.print_log(file_log, '\n\n## Standardized Precipitation Index (SPI)\n\n' +
                    sawbd.spi_desc +
                    '\n\n%s' %sawbd.precipitation_desc +
                    '\n\n* SPI index mobile average times: %s\n' %ppoi.times)

# SPI - Polygon processing
if polygon_eval:
    sawbf.print_log(file_log, '\n### Zonal analysis through N: %f°, S: %f°, E: %f°, W: %f°\n\n' % (lim_north, lim_south, lim_east, lim_west))
    da_data = xr.open_dataset(data_path+nc_file)
    da_data[feature_name[data_source_num]] = da_data[feature_name[data_source_num]] * units_mult
    ds_rr = da_data[feature_name[data_source_num]]
    year_min = sawbf.year_range_eval(da_data['time'], year_min, year_max)[0]
    year_max = sawbf.year_range_eval(da_data['time'], year_min, year_max)[1]
    sawbf.print_log(file_log, '#### NetCDF initial dataset\n\n```\n%s\n```\n\n#### Individual plots\n\n' %da_data)
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
            #print('Processing %s_spi_%s_%s (%d records)' % (data_source[data_source_num], str(i), str(year), da_count))
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
    # Export dataset with SPI calculations over ZE as .csv
    match data_source_num:
        case 0:  # CRU data
            da_data = da_data.sel(lon=slice(lim_west, lim_east), lat=slice(lim_south, lim_north),
                                  time=slice(str(year_min), str(year_max)))
        case 1:  # ERA5 reanalysis
            da_data = da_data.sel(longitude=slice(lim_west, lim_east), latitude=slice(lim_north, lim_south),
                             time=slice(str(year_min), str(year_max)))
        case _:
            print('\nAttention: datasource %s doesn''t exist or nor defined' %data_source_num)
    # Export .nc with SPI calculations over ZE as .csv & .nc
    df = da_data.to_dataframe()
    sawbf.print_log(file_log, '\n\n#### Output sliced datasets\n\n* Dataset as comma-separated values: [%s_spi_polygon.csv](spi/)' % data_source[data_source_num])
    df.to_csv(ppoi_path+'spi/'+str(data_source[data_source_num])+'_spi_polygon.csv', encoding='utf-8', index=True)
    if save_spi_nc:
        sawbf.print_log(file_log, '\n* Dataset as NetCDF: [%s_spi_polygon.nc](spi/)' % data_source[data_source_num])
        da_data.to_netcdf(ppoi_path+'spi/'+data_source[data_source_num]+'_spi_polygon.nc')
    sawbf.print_log(file_log, '\n\n```\n%s\n```' % da_data)
    # Gif animations
    sawbf.print_log(file_log, '\n\n#### Animations\n\nPrecipitation')
    p_gif = 'spi/'+data_source[data_source_num]+'/'
    key_name = data_source[data_source_num]+'_p'
    sawbf.make_gif(ppoi_path+p_gif, key_name, '.png')
    sawbf.print_log(file_log, '\n![R.SAWB](%s)' %(p_gif+key_name+'.gif'))
    for i in times:
        # print('\nCreating %s_spi_%d.gif' %(data_source[data_source_num], i))
        sawbf.print_log(file_log, '\n\nSPI-%d' % i)
        spi_gif = 'spi/' + data_source[data_source_num] + '/'
        key_name = data_source[data_source_num] + '_spi_' + str(i)
        sawbf.make_gif(ppoi_path+spi_gif, key_name, '.png')
        sawbf.print_log(file_log, '\n![R.SAWB](%s)' %(spi_gif+key_name+'.gif'))
    sawbf.print_log(file_log, '\n\nSPI records processed: %d\n' %records)

# SPI - Point processing
if point_eval:
    sawbf.print_log(file_log, '\n### Point analysis in Latitude: %f°, Longitude: %f° or nearest' %(point_latitude, point_longitude))
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
    p_fig = 'spi/'+data_source[data_source_num]+'_p_point'
    plt.savefig(ppoi_path+p_fig+'.png', dpi=dpi)
    if show_plot: plt.show()
    #sawbf.print_log(file_log, '\n\n#### Initial sliced dataframe')
    sawbf.print_log(file_log, '\n\n![R.SAWB](%s)\n' % (p_fig+'.png'))
    df = ds_rr_select.to_dataframe()
    sawbf.print_log(file_log,'\nDataset as comma-separated values: [%s_point.csv](spi/)' % data_source[data_source_num])
    sawbf.print_log(file_log, df.T.to_markdown(), center_div=True)
    point_csv_file = ppoi_path+p_fig+'.csv'
    df.to_csv(point_csv_file, encoding='utf-8', index=True)
    # SPI calculation
    data = pd.read_csv(point_csv_file)
    data['time'] = pd.to_datetime(data['time'])
    #print(data.dtypes)
    data = data.set_index('time')
    #print('\n\nData types:\n%s' %data.dtypes)
    for i in times:
        x = sawbf.spi_point(data[feature_name[data_source_num]], i)
        data['spi_' + str(i)] = x[9]
    #print('\nDataframe with SPI calculations\n', data)
    data.to_csv(ppoi_path+'spi/'+data_source[data_source_num]+'_spi_point.csv', encoding='utf-8', index=True)
    sawbf.print_log(file_log,'Dataset with SPI calculations as comma-separated values: [%s_spi_point.csv](spi/)\n' % data_source[data_source_num])
    sawbf.print_log(file_log, data.T.to_markdown(), center_div=True)
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
    spi_fig = 'spi/' + data_source[data_source_num] + '_spi_point.png'
    plt.savefig(ppoi_path+spi_fig, dpi=dpi)
    if show_plot: plt.show()
    plt.close('all')
    sawbf.print_log(file_log, '\n![R.SAWB](%s)\n' %spi_fig)

# *****************************************************************************************
# AWB - Post-processing procedure (ArcGIS for Desktop SAWB.tbx need to be run before)
# *****************************************************************************************
if awb_eval:
    sawbf.print_log(file_log, '\n## Atmospheric Water Balance (AWB) with ERA5 monthly through Latitude: %f°, Longitude: %f° or nearest\n' %(point_latitude, point_longitude))
    awb_dbf_files = glob.glob(ppoi_path + 'awb/q/' + '*.dbf')
    awb_df = pd.DataFrame()
    for i in awb_dbf_files:
        print('AWB - Processing: %s' %i)
        awb_dbf = DBF(i)
        awb_data_result = pd.DataFrame(iter(awb_dbf))
        awb_df = pd.concat([awb_df, awb_data_result], ignore_index=False)
    awb_year_min = awb_df['year'].min()
    awb_year_max = awb_df['year'].max()
    year_list = np.linspace(awb_year_min, awb_year_max, (awb_year_max-awb_year_min+1))
    sawbf.print_log(file_log, '\nProcessed years: %s' %year_list)
    awb_df['date'] = pd.to_datetime(awb_df['date'])
    awb_df.sort_values(by='date', inplace=True)
    print('\nDataframe types\n', awb_df.dtypes)
    awb_df = awb_df.set_index('date')
    sawbf.print_log(file_log, '\n\n### Initial processed dataset ([%s](awb/))\n\n%s\n\n' %(awb_q_join_file, awb_df.T.to_markdown()))
    sawbf.print_log(file_log, '%s' %sawbd.awb_dataset_vars)
    # Vapor flux serie
    awb_df.to_csv(ppoi_path+'awb/'+awb_q_join_file, encoding='utf-8', index=True)
    awb_df.plot(y='SUM', figsize=(10,6), title='AWB - Atmospheric accumulated vapor flux through Lat.: %f°, Lon.: %f° ' %(point_latitude, point_longitude), ylabel='Q, mm')
    q_fig = 'awb/graph/awb_q_serie.png'
    plt.savefig(ppoi_path+q_fig)
    if show_plot: plt.show()
    sawbf.print_log(file_log, '\n\n![R.SAWB](%s)' % q_fig )
    # Accumulation area serie
    awb_df.plot(y='Akm2', figsize=(10,6), title='AWB - Atmospheric accumulation area through Lat.: %f°, Lon.: %f° ' %(point_latitude, point_longitude), ylabel='A, km²')
    a_fig = 'awb/graph/awb_a_serie.png'
    plt.savefig(ppoi_path+a_fig)
    if show_plot: plt.show()
    sawbf.print_log(file_log, '\n\n![R.SAWB](%s)' % a_fig)
    # Vapor flux pivot
    pivot_table_q = awb_df.pivot_table(index='month', columns='year', values='SUM')
    sawbf.print_log(file_log, '\n\n### Atmospheric vapor flux - Pivot table ([%s](awb/))\n\n' % awb_q_pivot_file)
    q_pivot = ppoi_path+'awb/'+awb_q_pivot_file
    pivot_table_q.to_csv(q_pivot, encoding='utf-8', index=True)
    q_pivot_df = pd.read_csv(q_pivot, low_memory=False, index_col='month')
    sawbf.print_log(file_log, q_pivot_df.to_markdown())
    pivot_table_q.plot(y=year_list, figsize=(10,6), title='AWB - Atmospheric vapor flux through Lat.: %f°, Lon.: %f° ' %(point_latitude, point_longitude), ylabel='Q, mm')
    q_fig = 'awb/graph/awb_q_monthly.png'
    plt.savefig(ppoi_path+q_fig)
    if show_plot: plt.show()
    sawbf.print_log(file_log, '\n\n![R.SAWB](%s)' % q_fig)
    # Accumulation area pivot
    pivot_table_a = awb_df.pivot_table(index='month', columns='year', values='Akm2')
    sawbf.print_log(file_log, '\n\n### Atmospheric accumulation area (A) - Pivot table ([%s](awb/))\n\n' % awb_a_pivot_file)
    a_pivot = ppoi_path+'awb/'+awb_a_pivot_file
    pivot_table_a.to_csv(a_pivot, encoding='utf-8', index=True)
    a_pivot_df = pd.read_csv(a_pivot, low_memory=False, index_col='month')
    sawbf.print_log(file_log, a_pivot_df.to_markdown())
    pivot_table_a.plot(y=year_list, figsize=(10,6), title='AWB - Atmospheric accumulation area (A) through Lat.: %f°, Lon.: %f° ' %(point_latitude, point_longitude), ylabel='A, km²')
    # plt.xticks(range(len(pivot_table_a)),labels=range(0, len(pivot_table_a)))
    a_fig ='awb/graph/awb_a_monthly.png'
    plt.savefig(ppoi_path+a_fig)
    if show_plot: plt.show()
    sawbf.print_log(file_log, '\n\n![R.SAWB](%s)' % a_fig)
    plt.close('all')
    sawbf.print_log(file_log, '\n\nAWB records processed: %d\n' % len(awb_df))