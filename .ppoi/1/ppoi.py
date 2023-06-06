# Project point and polygon limits

# Research case information
sawb_client = 'r.cfdtools Researching Area'
sawb_order = 'rcfdtools-000000001'
sawb_date = '2023-05-30'  # yyyy-00-dd
sawb_title = 'Colombia - South America - Atmospheric water balance (AWB) and Drought analysis with the Standardized Precipitation Index (SPI)'
sawb_desc = 'The current research.....'

# SPI - Data source type and NetCDF file
data_source_num = 1  # 0:CRU, 1:ERA5-Reanalysis
# nc_file = 'cru_ts4.03.1901.2018.pre.dat.nc'
nc_file = 'ERA5Land_Monthly_01dd_ds1.nc'

# SPI index mobile average times
times = [1, 3]

# Units conversion multiplier & Maximum value for plotting ramp
# CRU data uses precipitation in millimeters
# ERA-5 reanalysis data uses precipitation in meters
units_mult = 1000  # ERA5 reanalysis
# units_mult = 1  # CRU
p_max_plot = 20  # ERA5 reanalysis with conversion to millimeters
# p_max_plot = 500  # CRU

# Study zone limit in decimal degrees, °dd
lim_north = 5.735
lim_south = 3.625
lim_east = -72.875
lim_west = -74.875
polygon_eval = True

# Point location in decimal degrees, °dd
point_latitude = 4.6
point_longitude = -73.7
point_eval = False

# Year range
year_min = 1980
year_max = 1982

# AWB
# Set awb_eval to False if you not executed ArcGIS for Desktop SAWB.tbx
awb_eval = False
