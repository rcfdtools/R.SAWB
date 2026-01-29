from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

meridians_sep = 10
point_latitude = 4.6
point_longitude = -73.7
lim_north = 16
lim_south = -58
lim_east = -25
lim_west = -96
figsize = (8, 8)

plt.figure(figsize=figsize)
map = Basemap(llcrnrlon=lim_west,llcrnrlat=lim_south,urcrnrlon=lim_east,urcrnrlat=lim_north,
             resolution='i', projection='lcc', lat_0 = 4.6, lon_0 = -73.7)
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral', lake_color='aqua')
#map.drawcoastlines()
map.readshapefile('../../.ppoi/1/awb/shpout/watershed/merge/watershed', 'watershed', drawbounds=True)
map.drawmeridians(np.arange(0, 360, meridians_sep))
map.drawparallels(np.arange(-90, 90, meridians_sep))
x, y = map(point_longitude, point_latitude)
plt.plot(x, y, 'ok', markersize=4, color='b')
plt.text(x, y, ' Lat: %s\nLon: %s)' % (point_latitude, point_longitude), fontsize=8);
plt.title('AWB atmospheric river areas')
parallels = np.arange(0., 81, meridians_sep)
map.drawparallels(parallels, labels=[False, True, True, False])
meridians = np.arange(10., 351., meridians_sep)
map.drawmeridians(meridians, labels=[True, False, False, True], rotation=45)
plt.show()