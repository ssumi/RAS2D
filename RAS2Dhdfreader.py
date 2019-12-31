# -*- coding: utf-8 -*-

"""

Created on Fri Apr 19 13:42:12 2019
@author: admin

"""

import os
import h5py                 #(if h5py is the cause for 'kernel died' pip uninstall h5py from anaconda and then pip install h5py)
#import shutil
import numpy as np
import pandas as pd
#from shutil import copyfile
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#from matplotlib.offsetbox import AnchoredText
import matplotlib.image as mpimg
#import seaborn as sns
from PIL import Image

os.chdir('E:\\Selina\\REALTIME_UPDATED_AND_OLD_FILES_HERE\\REALTIME_RAS\\Seth_Potomac_Anacostia\\VERSION0_MODEL_DEC2017_automate')
from NOAA_data_download import *

#--Change directory
os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model\\RASwithWatershed_v3')

#--Output file from HEC-RAS to be read in python

#hfile = 'Anacostia_Potomac_version1.p01.hdf'
hfile = 'Watershed1.p01.hdf'

#--Channel velocity,flow and water surface elevation
with h5py.File(hfile, 'r') as hf:
    
    wse1 = hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['2D Flow Areas']['Perimeter 1']['Water Surface']
    wse2  = np.array(wse1) 
    
    dep1 = hf['Results']['Unsteady']['Output']['Output Blocks']['Base Output']['Unsteady Time Series']['2D Flow Areas']['Perimeter 1']['Depth']
    dep2  = np.array(dep1) 
    
    
    cellxy = hf['Geometry']['2D Flow Areas']['Cell Points']
    cellxy  = np.array(cellxy) 
    
    #cellinfo = 
    
   # for index, key in enumerate(geom_info):
       # print(key)


#--Convert the required datasets into dataframe
dep =  pd.DataFrame.from_dict(dep2)       
wse =  pd.DataFrame.from_dict(wse2)
cellxy = pd.DataFrame.from_dict(cellxy)

#--Select cells
wse5479 = wse[5479]
wse8755 = wse[8755]
wse7285 = wse[7285]

dep5479 = dep[5479]
dep8755 = dep[8755]
dep7285 = dep[7285]


#--Plot cell depth and wse
wse5479.plot()
wse7285.plot()
wse8755.plot()

dep5479.plot()
dep8755.plot()
dep7285.plot()

#--Cell co-ordinate
cellxy5479 = cellxy.iloc[5479]

import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt

# Plot Grid shapefile
sf = shp.Reader("testfilepoly.shp")
#sf = shp.Reader("testfileflow.shp")
plt.figure()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    plt.plot(x,y)
plt.plot(cellxy5479[0],cellxy5479[1], marker='o',markersize = 8, color = 'r')

sf = shp.Reader("floodmap.shp")
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    plt.plot(x,y)
plt.show()

#Plot flood inundation boundary
import geopandas as gpd
shape=gpd.read_file('floodmap.shp')
shape.plot()


## Plot watershed
import geopandas as gp
watershed = gp.GeoDataFrame.from_file('testfile3.shp')
watershed.head()
watershed.plot()

import geopandas as gpd
gdf = gpd.read_file('testfile3.shp')
print(gdf)


###############################################################################
###############################################################################
# Read tif image
os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model')
# Open dataset
#import gdal
#ds = gdal.Open('Basinextend1.tif')
from osgeo import gdal
raster = gdal.Open( "tiftestdata.tif" )
print (gtif.GetMetadata())
gtif.GetProjection()
raster.RasterXSize
raster.RasterYSize
# Number of bands
raster.RasterCount
# Metadata for the raster dataset
raster.GetMetadata()
#-------------------------------
from osgeo import gdal
gdal.UseExceptions()
ds = gdal.Open('tiftestdata.tif')
band = ds.GetRasterBand(1)
band.SetNoDataValue(-3.402823e+38)
elevation = band.ReadAsArray()
print (elevation.shape)
print (elevation)
import matplotlib.pyplot as plt
plt.imshow(elevation, cmap='gist_earth')
plt.grid()
plt.show()
plt.plot(cellxy5479[0],cellxy5479[1], marker='o')
nrows, ncols = elevation.shape
x0, dx, dxdy, y0, dydx, dy = ds.GetGeoTransform()
x1 = x0 + dx * ncols
y1 = y0 + dy * nrows
plt.imshow(elevation, cmap='gist_earth', extent=[x0, x1, y1, y0])
plt.show()
elevation = ds.ReadAsArray()
# https://gis.stackexchange.com/questions/225370/get-individual-pixel-values-on-a-raster-image-using-gdal-and-python
from osgeo import gdal
import numpy as np
red = gdal.Open("tiftestdata.tif")
red_array = red.ReadAsArray().astype(np.float32)
print (red_array)
#------------------------------------------------------------------------------
# Read tif image
os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model')
from osgeo import gdal
from osgeo import gdal
import sys
# coordinates to get pixel values for (as tuples of points)
points = [(401229.289973, 4466415.48331)]
# open the raster file
ds = gdal.Open('tiftestdata.tif')
if ds is None:
    print ('Could not open the raster file')
    sys.exit(1)
else:
    print ('The raster file was opened satisfactorily')
# get georeference info
transform = ds.GetGeoTransform() # (-2493045.0, 30.0, 0.0, 3310005.0, 0.0, -30.0)
xOrigin = transform[0] # -2493045.0
yOrigin = transform[3] # 3310005.0
pixelWidth = transform[1] # 30.0
pixelHeight = transform[5] # -30.0
band = ds.GetRasterBand(1) # 1-based index
data = band.ReadAsArray()
# loop through the coordinates
for point in points:
    x = point[0]
    y = point[1]

    xOffset = int((x - xOrigin) / pixelWidth)
    yOffset = int((y - yOrigin) / pixelHeight)
    print (xOffset)
    print (yOffset)
    # get individual pixel values
    value = data[yOffset][xOffset]
    print (value)
#------------------------------------------------------------------------------
import rasterio
src = rasterio.open('tiftestdata.tif')
array = src.read(1)
array.shape
from matplotlib import pyplot
pyplot.imshow(array, cmap='pink')
with rasterio.open(array, 'r+') as f:
    f.write_mask(True)    
import rasterio
src = rasterio.open("tiftestdata.tif") 
src.shape
src.count
src.dtypes   
src.nodatavals
src.nodata
msk = src.read_masks(1)
os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model')
import shutil
import rasterio
tmp = shutil.copy("tiftestdata.tif", "tiftestdata2.tif")
src = rasterio.open(tmp, mode="r+")    
src.write_mask(True)    
src.read_masks(1).all()    
src.close()    
msk = src.read_masks()
pyplot.imshow(tmp, cmap='pink')
with rasterio.open('tiftestdata.tif', 'r+') as ds:
    arr = ds.read()  # read all raster values
    arr[0, 10, 20] = 3  # change a pixel value on band 1, row 11, column 21
    ds.write(arr)
# https://www.neonscience.org/classify-raster-thresholds-py   
chm_filename = 'tiftestdata.tif'
chm_dataset = gdal.Open(chm_filename)
#Display the dataset dimensions, number of bands, driver, and geotransform 
cols = chm_dataset.RasterXSize; print('# of columns:',cols)
rows = chm_dataset.RasterYSize; print('# of rows:',rows)
print('# of bands:',chm_dataset.RasterCount)
print('driver:',chm_dataset.GetDriver().LongName)
print('projection:',chm_dataset.GetProjection())
print('geotransform:',chm_dataset.GetGeoTransform())
noDataVal = chm_raster.GetNoDataValue(); print('no data value:',noDataVal)

import os
import sys
import time
import requests
import inspect
import pyautogui
import threading
import subprocess
from shutil import copyfile
import win32com.client      #link for the process: https://github.com/solomonvimal/PyFloods/blob/master/HEC_RAS_controller.py
from threading import Timer
from datetime import datetime, timedelta
os.chdir('E:\\Selina\\RAS2D\\RASTiles_Server_v1\RASTileServer')
subprocess.Popen("RASTiles.bat") 
E:\Selina\RAS2D\RASTiles_Server_v1\RASTileServer  
os.chdir('E:\\Selina\\RAS2D\\Potomac_RAS_Model\\RASwithWatershed_v3')


####

import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
sf = shp.Reader("floodmap.shp")
#sf = shp.Reader("testfileflow.shp")
plt.figure()
for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
    plt.plot(x,y)
plt.show()

#####

import geopandas as gp
watershed = gp.GeoDataFrame.from_file('testfile3.shp')
watershed.head()
watershed.plot()

import geopandas as gpd
gdf = gpd.read_file('testfile3.shp')
print(gdf)


import matplotlib.pyplot as plt
df = gpd.read_file(r'testfile3.shp')
import shapefile
sf=shapefile.Reader('testfile3.shp')
poly=sf.shape(1).__geo_interface__
fig = plt.figure() 
ax = fig.gca() 
ax.add_patch(PolygonPatch(poly, fc='#ffffff', ec='#000000', alpha=0.5, zorder=2 ))
ax.axis('scaled')
plt.show()