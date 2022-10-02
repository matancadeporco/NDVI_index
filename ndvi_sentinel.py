# -*- coding: utf-8 -*-
"""
# Created by Guilhermi M. Crispi at Fri May 28 11:02:28 2021

============================

Título: ndvi_python
Descrição: https://colekrehbiel.wordpress.com/2017/10/18/calculate-ndvi-from-sentinel-2a-data/

============================

"""

#%%
# Import libraries
import glob
import numpy as np
from osgeo import gdal
import scipy.misc as sm

# Set input directory
in_dir = '/Users/cole/Desktop/Website/Landsat/'

# Search directory for desired bands
b2_file = glob.glob(in_dir + '**B2.TIF') # blue band
b3_file = glob.glob(in_dir + '**B3.TIF') # green band
b4_file = glob.glob(in_dir + '**B4.TIF') # red band

# Define a function to normalize each band array by the min and max values
def norm(band):
    band_min, band_max = band.min(), band.max()
    return ((band - band_min)/(band_max - band_min))

# Loop through however many Landsat 8 obs are in the input directory 
for i in range(len(b2_file)):   
    
    # Open each band using gdal
    b2_link = gdal.Open(b2_file[i])
    b3_link = gdal.Open(b3_file[i])
    b4_link = gdal.Open(b4_file[i])
    
    # call the norm function on each band as array converted to float
    b2 = norm(b2_link.ReadAsArray().astype(np.float))
    b3 = norm(b3_link.ReadAsArray().astype(np.float))
    b4 = norm(b4_link.ReadAsArray().astype(np.float))
    
    # Create RGB
    rgb = np.dstack((b4,b3,b2))
    del b2, b3, b4
    
    # Visualize RGB
    #import matplotlib.pyplot as plt
    #plt.imshow(rgb)
    
    # Export RGB as TIFF file
    # Important: Here is where you can set the custom stretch
    # I use min as 2nd percentile and max as 98th percentile
    sm.toimage(rgb,cmin=np.percentile(rgb,2),
               cmax=np.percentile(rgb,98)).save(b2_file[i].split('_01_')[0]
               +'_RGB.tif')
                                                
                                                
#%% Import libraries
import glob
import numpy as np
from osgeo import gdal # If GDAL doesn't recognize jp2 format, check version

# Set input directory
in_dir = '/Users/cole/Desktop/Sentinel/'

# Search directory for desired bands
red_file = glob.glob(in_dir + '**B04.jp2') # red band
nir_file = glob.glob(in_dir + '**B08.jp2') # nir band

# Define a function to calculate NDVI using band arrays for red, NIR bands
def ndvi(red, nir):
    return ((nir - red)/(nir + red))
    
# Open each band using gdal
red_link = gdal.Open(red_file[0])
nir_link = gdal.Open(nir_file[0])
    
# read in each band as array and convert to float for calculations
red = red_link.ReadAsArray().astype(np.float)
nir = nir_link.ReadAsArray().astype(np.float)

# Call the ndvi() function on red, NIR bands
ndvi2 = ndvi(red, nir)

# Create output filename based on input name 
outfile_name = red_file[0].split('_B')[0] + '_NDVI.tif'

x_pixels = ndvi2.shape[0]  # number of pixels in x
y_pixels = ndvi2.shape[1]  # number of pixels in y

# Set up output GeoTIFF
driver = gdal.GetDriverByName('GTiff')

# Create driver using output filename, x and y pixels, # of bands, and datatype
ndvi_data = driver.Create(outfile_name,x_pixels, y_pixels, 1,gdal.GDT_Float32)

# Set NDVI array as the 1 output raster band
ndvi_data.GetRasterBand(1).WriteArray(ndvi2)

# Setting up the coordinate reference system of the output GeoTIFF
geotrans=red_link.GetGeoTransform()  # Grab input GeoTranform information
proj=red_link.GetProjection() # Grab projection information from input file

# now set GeoTransform parameters and projection on the output file
ndvi_data.SetGeoTransform(geotrans) 
ndvi_data.SetProjection(proj)
ndvi_data.FlushCache()
ndvi_data=None