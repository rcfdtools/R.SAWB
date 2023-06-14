import pandas as pd
import geopandas as gpd
import glob

ppoi_num = 1  # <<<<<<<< PPOI number to process
ppoi_path = '../../.ppoi/'+str(ppoi_num)+'/'

shpout_class = ['basindissolve', 'watershed']
for d in shpout_class:
    shpout_path = ppoi_path + 'awb/shpout/'+d+'/'
    shp_files = glob.glob(shpout_path+'*.shp')
    print(shp_files)
    # Creating empty shapefile
    shp_merge = d+'.shp'
    #schema = {"geometry": "Polygon", "properties": {"id": "int"}}
    schema = {"geometry": "Polygon"}
    crs = "EPSG:4326"
    shp = gpd.GeoDataFrame(geometry=[])
    shp.to_file(shpout_path+'merge/'+shp_merge, driver='ESRI Shapefile', schema=schema, crs=crs)
    shp = gpd.read_file(shpout_path+'merge/'+shp_merge)
    for i in shp_files:
        gdf = gpd.read_file(i)
        shp = gpd.GeoDataFrame(pd.concat([gdf, shp]))
    shp.to_file(shpout_path+'merge/'+shp_merge)
