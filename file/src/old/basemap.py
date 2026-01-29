import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
from itertools import chain

def draw_map(m, scale=0.2):
    # draw a shaded-relief image
    # Function from https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
    m.shadedrelief(scale=scale)

    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)

    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')

# Vars
point_latitude = 4.6
point_longitude = -73.7
meridians_sep = 10
lim_north = 5.735
lim_south = 3.625
lim_east = -72.875
lim_west = -74.875
'''
lim_north = 16
lim_south = -58
lim_east = -25
lim_west = -96
'''

# Global map
'''
fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='ortho', resolution=None, lat_0=4, lon_0=-72)
m.bluemarble(scale=0.5);
plt.show()
'''

# Point map
'''
fig = plt.figure(figsize=(16, 8), edgecolor='w')
m = Basemap(projection='lcc', resolution='l',
            width=8E6, height=4E6,
            lat_0=point_latitude, lon_0=point_longitude)
m.shadedrelief(scale=0.5, alpha=1)
m.drawcoastlines(color='black', linewidth=0.25)
m.drawcountries(color='gray')
m.drawstates(color='gray')
# Map (long, lat) to (x, y) for plotting
x, y = m(-73.7, 4.6)
plt.plot(x, y, 'ok', markersize=3)
plt.text(x, y, ' Study point', fontsize=10);
plt.show()
'''

# Perspective projections
'''
fig = plt.figure(figsize=(16, 8), edgecolor='w')
m = Basemap(projection='lcc', resolution='l',
            width=8E6, height=4E6,
            lat_0=point_latitude, lon_0=point_longitude)
x, y = m(-73.7, 4.6)
plt.plot(x, y, 'ok', markersize=3)
plt.text(x, y, ' Study point', fontsize=10);
draw_map(m);
plt.show()
'''

# Point location
# https://matplotlib.org/basemap/users/examples.html
projection = ['ortho', 'lcc']
for i in projection:
    if i == 'ortho':
        fig = plt.figure(figsize=(8, 8))
        title = 'Global location'
        meridians_sep = meridians_sep * 2
    else:
        fig = plt.figure(figsize=(16, 8))
        title = 'Regional location'
        meridians_sep = meridians_sep
    map = Basemap(projection=i, lat_0=point_latitude, lon_0=point_longitude, resolution='l', width=8E6, height=4E6)
    map.drawcountries(linewidth=0.25)
    map.drawcoastlines(linewidth=0.35)
    map.fillcontinents(color='coral', lake_color='aqua', alpha=1)
    map.drawmapboundary(fill_color='aqua')
    map.drawmeridians(np.arange(0,360,meridians_sep))
    map.drawparallels(np.arange(-90,90,meridians_sep))
    x, y = map(point_longitude, point_latitude)
    plt.plot(x, y, 'ok', markersize=3)
    plt.text(x, y, ' PPOI (Lat: %s, Lon: %s)' %(point_latitude, point_longitude), fontsize=10);
    plt.title(title)
    parallels = np.arange(0., 81, meridians_sep)
    map.drawparallels(parallels, labels=[False, True, True, False])
    meridians = np.arange(10., 351., meridians_sep)
    map.drawmeridians(meridians, labels=[True, False, False, True], rotation=45)
    plt.show()

# Polygon location
# https://matplotlib.org/basemap/users/examples.html
# https://stackoverflow.com/questions/12251189/how-to-draw-rectangles-on-a-basemap
map_polygon_scale_factor = 4  # 1 for Colombia country, 4 for South America
meridians_sep = meridians_sep * 2
lat_0 = lim_north-(lim_north-lim_south)/2
lon_0 = lim_east-(lim_east-lim_west)/2
width = abs((lim_east-lim_west)/map_polygon_scale_factor)*1e6
height = abs((lim_north-lim_south)/map_polygon_scale_factor)*1e6
base_value = 8
aspect_ratio = abs(height/width)
if height > width:
    fig_size_height = base_value * aspect_ratio
    fig_size_width = base_value
else:
    fig_size_height = base_value
    fig_size_width = base_value * aspect_ratio
fig = plt.figure(figsize=(fig_size_width, fig_size_height))
map = Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0, resolution='l', width=width, height=height)
map.drawcountries(linewidth=0.25)
map.drawcoastlines(linewidth=0.35)
map.fillcontinents(color='coral', lake_color='aqua')
map.drawmapboundary(fill_color='aqua')
map.drawmeridians(np.arange(0,360,meridians_sep))
map.drawparallels(np.arange(-90,90,meridians_sep))
x1,y1 = map(lim_east, lim_north)
x2,y2 = map(lim_west, lim_north)
x3,y3 = map(lim_west, lim_south)
x4,y4 = map(lim_east, lim_south)
poly = Polygon([(x1,y1), (x2,y2), (x3,y3), (x4,y4)], facecolor=None, edgecolor='black', linewidth=1.5, alpha=0.5)
plt.gca().add_patch(poly)
x, y = map(lon_0, lat_0)
plt.plot(x, y, 'ok', markersize=0)
plt.text(x, y, ' Case zone (centroid Lat: %s, Lon: %s)' %(lat_0, lon_0), fontsize=10);
plt.title('Polygon location')
parallels = np.arange(0., 81, meridians_sep)
map.drawparallels(parallels, labels=[False, True, True, False])
meridians = np.arange(10., 351., meridians_sep)
map.drawmeridians(meridians, labels=[True, False, False, True], rotation=45)
plt.show()


# References
# https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
