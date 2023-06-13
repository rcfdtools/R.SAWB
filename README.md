# R.SAWB
Keywords: `SWB` `AWB` `SPI` `ERA5` `CRU` 

Surface Water Balance (SWB) &amp; Atmospheric Water Balance (AWB) &amp; Standardized Precipitation Index (SPI)

AWB

P: precipitation in millimeters
E: evaporation in millimeters
Q: vapor flux vector in millimeters


## Pending tasks

* General localization map (polygon and point). AWB post-processing - year list from q folder.
* General statistics over the data source file .nc and the study zone. Pmin, Pmax, Pavg, Pstd, Emin, Emax, Eavg, Estd.
* Drop `expver` values and featura. `expver` is used to tell the difference between the initial release (expver=5, called ERA5T) and validated ERA5 data (expver=1). https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation
* Merge atmospheric basin shapefiles into a unique shapefile
* Plot title with datasource information
* Log record separators in console
* Rain and evaporation time series over point and polygon. P-E. Graph and table
* PPOI GeoJson map
* Location map, world. Rectangle data source, rectangle study zone, point. See https://docs.xarray.dev/en/stable/user-guide/plotting.html
* Technical documentation for scientific articles. See https://edo.jrc.ec.europa.eu/documents/factsheets/factsheet_spi_ado.pdf
* Download ERA5 1 hour 0.25dd with full Earth coverage. 1 day aggregation
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
* Integrated script sawb.py for run all the proceses. SPI & AWS post-processing are integrated
* Gif animations for time-series data map
* Scientific Markdown report for each PPOI and data source. (Note: SPI can run with CRU or EAR5 datasets. The current AWB script only works with EAR-5 monthly datasets). AWB results links. AWB variable description obtained from Model Builder. 


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

> Python requires a Virtual Environment for the script executions and the libraries described in the file `Requirements.txt`. From the Terminal execute `pip install -r requirements.txt`


## File compression

Windows CMD sample: "C:\Program Files\7-Zip\7z.exe" a -v97m "D:\R.SAWB\.nc\File.zip" "D:\R.SAWB\.nc\cru_ts4.03.1901.2018.pre.dat.nc"


## References

* [Conjoint Analysis of Surface and Atmospheric Water Balances in the Andes-Amazon System](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2017WR021338)
* [An Atmospheric Water Balance Perspective on Extreme Rainfall Potential for the Contiguous US](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020WR028387)
* [Atmospheric water balance over oceanic regions as estimated from satellite, merged, and reanalysis data](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/jgrd.50414)
* Global Atmospheric Water Balance and Runoff from Large River Basins
* https://stackoverflow.com/questions/41898561/pandas-transform-a-dbf-table-into-a-dataframe
* https://sparkbyexamples.com/pandas/sort-pandas-dataframe-by-date/
* https://www.dataquest.io/blog/plot-dataframe-pandas/
* https://www.geeksforgeeks.org/numpy-linspace-python/
* https://www.caee.utexas.edu/prof/maidment/gishyd97/atmos/atmos.htm
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
* https://www.datacamp.com/tutorial/python-subprocess
* https://www.kdnuggets.com/2020/09/geographical-plots-python.html
* https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
* https://notebook.community/milancurcic/lunch-bytes/Fall_2019/LB33/Basemap_v_Cartopy
* https://matplotlib.org/basemap/users/examples.html
* https://stackoverflow.com/questions/12251189/how-to-draw-rectangles-on-a-basemap
