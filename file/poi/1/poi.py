# Project point and polygon limits

# Research case information
sawb_client = 'r.cfdtools Researching Area'
sawb_order = 'rcfdtools-000000001'
sawb_date = '2023-05-30'  # yyyy-00-dd
sawb_title = 'Colombia - South America - Atmospheric water balance (AWB) and Drought analysis with the Standardized Precipitation Index (SPI)'
sawb_desc = 'This study contains an estimate the Standardized Precipitation Index (SPI) and the water balance over the defined study zone and the convergence to the one specific point using the atmospheric water balance method (AWB).'

# Global parameters
meridians_sep = 10  # Separation between meridians or parallels in decimal degrees
map_polygon_scale_factor = 3  # e.g. 1 for Colombia country, 4 for South America
year_min = 1980  # SPI - Initial year
year_max = 1989  # SPI - Final year
times = [1, 3, 6]  # SPI - Index mobile average times

# SPI - Data source type and NetCDF file
data_source_num = 1  # 0:CRU, 1:ERA5-Reanalysis
# nc_file = 'cru_ts4.03.1901.2018.pre.dat.nc'
nc_file = 'ERA5Land_Monthly_01dd_ds1.nc'

# Units conversion multiplier & Maximum value for plotting ramp
# CRU data uses precipitation in millimeters
# ERA-5 reanalysis data uses precipitation in meters
units_mult = 1000  # ERA5 reanalysis
# units_mult = 1  # CRU
p_max_plot = 20  # ERA5 reanalysis with conversion to millimeters
# p_max_plot = 500  # CRU

# SPI - Study zone limits in decimal degrees, °dd
lim_north = 14.
lim_south = -4.8
lim_east = -66.
lim_west = -82.5
polygon_eval = True

# SPI - Point location in decimal degrees, °dd
point_latitude = 4.6
point_longitude = -73.7
point_eval = True

# AWB
# Set awb_eval to False if you don't execute yet the ArcGIS for Desktop toolbox SAWB.tbx
# Limits are used for the atmospheric river areas representations. May coincide with the original .nc file used
lim_north_awb = 16
lim_south_awb = -58
lim_east_awb = -25
lim_west_awb = -96
awb_eval = True
