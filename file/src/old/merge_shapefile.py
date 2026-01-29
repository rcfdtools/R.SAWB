import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import glob
import os

ppoi_num = 1  # <<<<<<<< PPOI number to process
ppoi_path = '../../.ppoi/'+str(ppoi_num)+'/'
show_plot = False  # Verbose plot
figsize = (5, 5)
dpi = 128  # Save plot resolution

shpout_class = ['basindissolve', 'watershed']
for d in shpout_class:
    shpout_path = ppoi_path + 'awb/shpout/'+d+'/'
    shp_files = glob.glob(shpout_path+'*.shp')
    #print(shp_files)
    # Creating the merged empty shapefile
    shp_merge = d+'.shp'
    #schema = {"geometry": "Polygon", "properties": {"id": "int"}}
    schema = {"geometry": "Polygon"}
    crs = "EPSG:4326"
    shp = gpd.GeoDataFrame(geometry=[])
    shp.to_file(shpout_path+'merge/'+shp_merge, driver='ESRI Shapefile', schema=schema, crs=crs)
    shp = gpd.read_file(shpout_path+'merge/'+shp_merge)
    shp.to_crs(epsg=4326)
    # Concatenating the shapefiles (required for time-series representations over ArcGIS or QGIS)
    for i in shp_files:
        print('Processing: %s' % i)
        basename = os.path.basename(i)
        gdf = gpd.read_file(i)
        legend = True
        cmap = 'rainbow'
        if d == 'watershed':
            legend = False
            cmap = 'coolwarm'
        gdf.plot(column='GRIDCODE', linewidth=0.0, legend=legend, edgecolor=None, figsize=figsize, alpha=1, cmap=cmap, legend_kwds={'label': 'Gridcode', 'orientation': 'vertical'})
        if show_plot: plt.show()
        plt.title('AWB - ' + basename)
        plt.xlabel('Lon.°')
        plt.ylabel('Lat.°')
        #plt.legend(title='Gridcode')
        plt.savefig(ppoi_path + 'awb/shpout/'+d+'/graph/' + basename + '.png', dpi=dpi)
        plt.close()
        shp = gpd.GeoDataFrame(pd.concat([gdf, shp]))
    shp.to_file(shpout_path+'merge/'+shp_merge)
