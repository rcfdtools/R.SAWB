# R.SAWB
Surface Water Balance (SWB) &amp; Atmospheric Water Balance (AWB)  

Data source: https://cds.climate.copernicus.eu/

## Searching data from ERA-5

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


## References

* https://www.caee.utexas.edu/prof/maidment/gishyd97/atmos/atmos.htm
* [Conjoint Analysis of Surface and Atmospheric Water Balances in the Andes-Amazon System](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2017WR021338)
* https://edo.jrc.ec.europa.eu/documents/factsheets/factsheet_spi_ado.pdf
* [How to calculate PET, SPI, SPEI and Palmer drought indices in Python?](https://www.youtube.com/watch?v=WMF45KQiQAM)
* [Standardized Precipitation Index (SPI) | Drought & Flood Monitor](https://www.youtube.com/watch?v=zYT5VpQWJAQ)
* https://climatedataguide.ucar.edu/climate-data/standardized-precipitation-index-spi
* https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.03/cruts.1905011326.v4.03/pre/
* https://stackoverflow.com/questions/57507832/unable-to-allocate-array-with-shape-and-data-type
* https://ado.eurac.edu/spi-6