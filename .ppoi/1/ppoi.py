# Project point and polygon limits

# Research information
sawb_client = 'r.cfdtools Research Center'
sawb_order = '1'
sawb_date = '2023-05-30'  # yyyy-00-dd
sawb_desc = 'Colombia - South Americas - Drought analysis using the Standarized Precipitation Index - SPI and Atmospheric water balance - AWB'

# Data source NetCDF file
nc_file = 'cru_ts4.03.1901.2018.pre.dat.nc'
#nc_file = 'ERA5Land_Monthly_01dd.nc'
data_source_num = 0  # 0:CRU, 1:ERA5-Reanalysis

# Point location in decimal degrees °
point_latitude = 4.6
point_longitude = -73.7

# Study zone limit in decimal degrees °
lim_north = 14
lim_south = -4.8
lim_east = -66
lim_west = -82.5

# Year range
year_min = 1980
year_max = 1982

# SPI index mobile average times
times = [1, 3]

# Units conversion multiplier & Maximum value for plotting ramp
# CRU data uses precipitation in millimeters
# ERA-5 reanalysis data uses precipitation in meters
#units_mult = 1000  # ERA5 reanalysis
units_mult = 1  # CRU
#p_max_plot = 20  # ERA5 reanalysis with conversion to milimeters
p_max_plot = 500  # CRU