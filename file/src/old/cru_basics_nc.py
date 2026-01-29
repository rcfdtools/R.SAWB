import xarray as xr
import matplotlib.pyplot as plt

path = '../../.nc/'
nc_file = 'cru_ts4.03.1901.2018.pre.dat.nc'
feature_name = 'pre'
interline = '-'
interlen = 100
separator = interlen*interline
p_max_plot = 250  # Maximum value for plotting ramp
show_plot = False  # Verbose plot
prefix_file = 'cru'
# Point location
point_latitude = 4.6
point_longitude = -73.7
# Study zone limits
lim_north = 5.735
lim_south = 3.625
lim_east = -72.875
lim_west = -74.875
year_sample = '2010'
dpi = 128  # Save plot resolution

# Datasets & DataArrays
ds = xr.open_dataset(path+nc_file)
rr = ds[feature_name]
print('%s\nDataset: %s\n%s\n' %(separator, nc_file, separator), ds,'\n')
print('%s\nVariables founded\n%s\n' %(separator, separator), ds.data_vars,'\n')
print('%s\nFeature: %s\n%s\n' %(separator, feature_name, separator), rr,'\n')
print('%s\nAttributes items\n%s\n' %(separator, separator), ds.attrs.items(),'\n')

# Selecting point location & export to .csv file
rr_select = rr.sel(lon=point_longitude, lat=point_latitude, method='nearest')
print('%s\nFeature point: %s in Lat:%f, Lon: %f nearest\n%s\n' %(separator, feature_name, point_latitude, point_longitude, separator), rr_select,'\n')
rr_select.plot(figsize=(10,6))
plt.savefig('../../.temp/cru/' + 'P_point.png', dpi=dpi)
if show_plot: plt.show()
df = rr_select.to_dataframe()
print(df)
df.to_csv('../../.temp/cru/'+prefix_file+'_xarray_basics_point.csv', encoding='utf-8', index=True)

# Areal slice & export to .csv file
rr_select = rr.sel(lon=slice(lim_west, lim_east), lat=slice(lim_south, lim_north))
print('%s\nFeature zone: %s in North: %f, South: %f, East: %f, West: %f\n%s\n' %(separator, feature_name, lim_north, lim_south, lim_east, lim_west, separator), rr_select,'\n')
rr_select.plot(figsize=(10,6))
plt.savefig('../../.temp/cru/' + 'P_ze_hist.png', dpi=dpi)
if show_plot: plt.show()
df = rr_select.to_dataframe()
print(df)
df.to_csv('../../.temp/cru/'+prefix_file+'_xarray_basics_ze.csv', encoding='utf-8', index=True)

# Areal slice in a specific year
rr.sel(time=year_sample).plot(cmap='YlGnBu', col='time', col_wrap=4, vmin=0, vmax=p_max_plot)
plt.ylim(lim_south, lim_north)
plt.xlim(lim_west, lim_east)
plt.savefig('../../.temp/cru/' + 'P_' + str(year_sample) + '.png', dpi=dpi)
if show_plot: plt.show()


# References
# https://www.youtube.com/watch?v=1a2yqIltVT8
# https://github.com/jeffjay88/Climate_Indices





