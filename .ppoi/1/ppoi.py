# Project point and polygon limits

# Research information
sawb_client = 'r.cfdtools Research Center'
sawb_order = '1'
sawb_date = '2023-05-30'  # yyyy-00-dd
sawb_desc = 'South Americas drought analysis using the Standarized Precipitation Index - SPI and Atmospheric water balance - AWB.'

# Data source NetCDF file
#nc_file = 'cru_ts4.03.1901.2018.pre.dat.nc'
nc_file = 'ERA5Land_Monthly_01dd.nc'
data_source_num = 1  # 0:CRU, 1:ERA5-Reanalysis

# Point location in decimal degrees °
point_latitude = 4.6
point_longitude = -73.7

# Study zone limit in decimal degrees °
lim_north = 16
lim_south = -58
lim_east = -25
lim_west = -96

# Year range
year_min = 1980
year_max = 1982

# SPI index mobile average times
times = [1, 3]

# Maximum value for plotting ramp
# CRU data uses precipitation in millimeters
# ERA-5 reanalysis data uses precipitation in meters
p_max_plot = 0.02  # ERA5 reanalysis
#p_max_plot = 500  # CRU