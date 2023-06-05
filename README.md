# R.SAWB
Surface Water Balance (SWB) &amp; Atmospheric Water Balance (AWB)  

Data source: https://cds.climate.copernicus.eu/


## Pending tasks

* Gif and video animation for temporal map data
* General statistics over the data source file .nc and the study zone
* Merge atmospheric basin shapefiles into a unique shapefile
* Plot title with datasource information
* Log record separators in console
* Rain and evaporation time series over point and polygon. P-E. Graph and table
* PPOI GeoJson map
* Location map, world. Rectangle data source, rectangle study zone, point. See https://docs.xarray.dev/en/stable/user-guide/plotting.html
* Scientific Markdown report for each PPOI and data source
* Technical documentation for scientific articles. See https://edo.jrc.ec.europa.eu/documents/factsheets/factsheet_spi_ado.pdf
* Compress .nc & .csv into .zip files for GitHub massive uploads (95MB part files)


## [sawb.py](.src/sawb.py) features

* Execution over different data sources as CRU or ERA5 reanalysis.
* Maximum precipitation value for map plots
* Spatial zone to evaluate
* Temporal time serie segmentation
* Export the original features and the SPI features in NetCFD (.nc) and comma separated values (.csv)
* SPI calculation over multiple moving window of n months defined by the user
* Precipitation & SPI yearly maps per month (for a range of accumulation periods). Classification and palette color for SPI Classification following McKee et al. (1993) 
* Exception control for years outside the available data limit, e.g. the datafile .nc contains values between 1980-2022 and the user set a range between 1970-2022.
* Research point and polygon `ppoi.py` contains the parameters required for the execution, like description, order #, date and description, data source, point location and polygon limits, year ranges, mobile average times, units conversions multipliers and the maximum values used as references for the map global palettes.
* Units conversion, e.g. m to mm for rain or evaporation parameters
* Polygon processing on demand with limits defined by user
* Point processing on demand with coordinates defined by user
* Creates PPOI folder structures for new case studies. The file [.ppoi/1/ppoi.py](.ppoi/1/ppoi.py) used as template.
* Purge last results before a new running
* Global definitions dictionary as spi_dictionary.py
* Validate and fix range year_min > year_max
* Integrated script sawb.py for run all the proceses. SPI & AWS post-processing are integrated.


## Searching data from ERA5

### Search 1: ERA5-Land monthly averaged data from 1950 to present
	
* Resolution: 0.1dd x 0.1dd
* Submission date: 2023-05-06 10:13:33
* Size: 1.0 GB+
* Product type: Monthly averaged reanalysis
* Variables: 10m u-component of wind, 10m v-component of wind, 2m temperature, Total evaporation, Total precipitation
* Year: 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2022
* Month: January, February, March, April, May, June, July, August, September, October, November, December
* Time: 00:00
* Sub-region extraction: North 16°, West -96°, South -58°, East -25°
* Format:GRIB & NetCDF

Limits - South America

lim_north = 16
lim_south = -58
lim_east = -25
lim_west = -96

Limits - Colombia - South America

lim_north = 14
lim_south = -4.8
lim_east = -66
lim_west = -82.5

Limits - Colombia - South America - Bogotá Chingaza

* lim_north = 5.735
* lim_south = 3.625
* lim_east = -72.875
* lim_west = -74.875


### Search 2: ERA5 hourly data on single levels from 1940 to present (land & seas)

* Resolution: 0.25dd x 0.25dd
* Variables: 10m u-component of wind, 10m v-component of wind, 2m temperature, Evaporation, Total precipitation


### Search 3: ERA5 monthly averaged data on single levels from 1940 to present (land & sea)
	
* Resolution: 0.25dd x 0.25dd
* Variables: 10m u-component of wind, 10m v-component of wind, 2m temperature, Evaporation, Total precipitation


## System configuration for big NetCDF files over Windows 11

1. Press the <kbd>Windows</kbd> + <kbd>R</kbd> keys on your keyboard to open the Run dialog.
2. Type `sysdm.cpl` in the text box and press <kbd>Enter</kbd>. The System Properties menu will open.
3. Navigate to the `Advanced` tab. You are now in the Advanced System Settings menu.
4. Under `Performance`, clic on `Settings`.
5. Under `Performance Options`, navigate to the `Advanced` tab.
6. Under the `Virtual memory` section, clic on `Change`.
7. Uncheck the box `Automatically manage paging file size for all drives`.
8. Select the Drive C: and set a virtual memory custom size with Initial size in 5120Mb and Maximum size in 10240Mb. 
9. Clic on `OK`, `Apply`, `Ok`.
10. Restart your Windows system.

> You can also set a custom size virtual memory for the drives where your data processing is running.
> 
> The specific virtual memory size depends on the size of your NetCDF files.


## Execution procedure

1. From ArcGIS for Desktop 10.2.2, run the ArcToolBox `SAWB.tbx/a. Monthly Balance`
2. From Python run the script `.src/spi.py`
3. From Python run the script `.src/sawb_monthly_poi.py`


## File compression

Windows CMD sample: "C:\Program Files\7-Zip\7z.exe" a -v97m "C:\R.SAWB\.nc\File.zip" "C:\R.SAWB\.nc\cru_ts4.03.1901.2018.pre.dat.nc"


## References

* https://stackoverflow.com/questions/41898561/pandas-transform-a-dbf-table-into-a-dataframe
* https://sparkbyexamples.com/pandas/sort-pandas-dataframe-by-date/
* https://www.dataquest.io/blog/plot-dataframe-pandas/
* https://www.geeksforgeeks.org/numpy-linspace-python/
* https://www.caee.utexas.edu/prof/maidment/gishyd97/atmos/atmos.htm
* [Conjoint Analysis of Surface and Atmospheric Water Balances in the Andes-Amazon System](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2017WR021338)
* https://edo.jrc.ec.europa.eu/documents/factsheets/factsheet_spi_ado.pdf
* [Standardized Precipitation Index (SPI) | Drought & Flood Monitor](https://www.youtube.com/watch?v=zYT5VpQWJAQ)
* https://climatedataguide.ucar.edu/climate-data/standardized-precipitation-index-spi
* https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.03/cruts.1905011326.v4.03/pre/
* https://stackoverflow.com/questions/57507832/unable-to-allocate-array-with-shape-and-data-type
* https://ado.eurac.edu/spi-6
* https://matplotlib.org/stable/tutorials/colors/colormaps.html
* [Read and plot netCDF file in python | easy method to handle netcdf files - Include vector limits](https://www.youtube.com/watch?v=eoIS68sSvGI)
* [Xarray Basics | Fundamentals of Xarray That Could Be Helpful for Data Science and Analytics](https://www.youtube.com/watch?v=1a2yqIltVT8)
* [Timeseries Analysis using Python Xarray](https://www.youtube.com/watch?v=Ndfo967JgSY)
* https://docs.xarray.dev/en/stable/user-guide/plotting.html
* https://es.wikipedia.org/wiki/Crisis_energ%C3%A9tica_de_1992_en_Colombia
* https://realpython.com/python-zipfile/
* https://github.com/jeffjay88/Climate_Indices
* https://www.blog.pythonlibrary.org/2021/06/23/creating-an-animated-gif-with-python/
* https://stackoverflow.com/questions/11067097/7zip-commands-from-python

