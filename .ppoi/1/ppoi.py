# Project point and polygon limits

# Research information
sawb_client = 'r.cfdtools Research Center'
sawb_order = '1'
sawb_date = '2023-05-30'  # yyyy-00-dd
sawb_title = 'Colombia - South America - Drought analysis using the Standardized Precipitation Index - SPI and Atmospheric water balance - AW'
sawb_desc = 'The Standardized Precipitation Index (SPI) is a widely used index to characterize meteorological drought on a range of timescales. On short timescales, the SPI is closely related to soil moisture, while at longer timescales, the SPI can be related to groundwater and reservoir storage. The SPI can be compared across regions with markedly different climates. It quantifies observed precipitation as a standardized departure from a selected probability distribution function that models the raw precipitation data. The raw precipitation data are typically fitted to a gamma or a Pearson Type III distribution, and then transformed to a normal distribution. The SPI values can be interpreted as the number of standard deviations by which the observed anomaly deviates from the long-term mean. The SPI can be created for differing periods of 1-to-36 months, using monthly input data. For the operational community, the SPI has been recognized as the standard index that should be available worldwide for quantifying and reporting meteorological drought. Concerns have been raised about the utility of the SPI as a measure of changes in drought associated with climate change, as it does not deal with changes in evapotranspiration. [(NCAR)](https://climatedataguide.ucar.edu/climate-data/standardized-precipitation-index-spi)'

# Data source NetCDF file
nc_file = 'cru_ts4.03.1901.2018.pre.dat.nc'
# nc_file = 'ERA5Land_Monthly_01dd.nc'
data_source_num = 0  # 0:CRU, 1:ERA5-Reanalysis

# Study zone limit in decimal degrees, °dd
lim_north = 14
lim_south = -4.8
lim_east = -66
lim_west = -82.5
polygon_eval = False

# Point location in decimal degrees, °dd
point_latitude = 4.6
point_longitude = -73.7
point_eval = True

# Year range
year_min = 1980
year_max = 2022

# SPI index mobile average times
times = [1, 3]


# Units conversion multiplier & Maximum value for plotting ramp
# CRU data uses precipitation in millimeters
# ERA-5 reanalysis data uses precipitation in meters
# units_mult = 1000  # ERA5 reanalysis
units_mult = 1  # CRU
# p_max_plot = 20  # ERA5 reanalysis with conversion to milimeters
p_max_plot = 500  # CRU
