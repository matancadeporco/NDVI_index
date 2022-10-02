# -*- coding: utf-8 -*-
"""
# Created by Guilhermi M. Crispi at Fri May 28 11:02:28 2021

============================

Título: ndvi gdal python
Descrição:  https://hatarilabs.com/ih-en/how-to-calculate-vegetation-index-ndvi-from-sentinel2-with-pyqgis
    arquivos necessários: http://download.osgeo.org/gdal/win32/1.6/

============================

"""

#%%
import os
from osgeo import gdal,gdal_array

#%%

os.chdir("/Users/guillh/Documents/Sentinel2Clip")
print(os.listdir(os.getcwd()))

NIR = iface.addRasterLayer('clip_RT_S2A_OPER_MSI_L1C_TL_MTI__20160506T214824_A004555_T18LTM_B08.tif','NIR')
RED = iface.addRasterLayer('clip_RT_S2A_OPER_MSI_L1C_TL_MTI__20160506T214824_A004555_T18LTM_B04.tif','RED')

import processing

NIR = processing.getObjectFromName("NIR")
RED = processing.getObjectFromName("RED")

NDVI_syntax = '(A-B)/(A+B)'

outputs_GDALOGRRASTERCALCULATOR_1=processing.runalg('gdalogr:rastercalculator', 
                                                    NIR,         #INPUT_A <ParameterRaster>
                                                    '1',         #BAND_A <ParameterString>
                                                    RED,         #INPUT_B <ParameterRaster>
                                                    '1',         #BAND_B <ParameterString>
                                                    None,        #INPUT_C <ParameterRaster>
                                                    '1',         #BAND_C <ParameterString>
                                                    None,        #INPUT_D <ParameterRaster>
                                                    '1',         #BAND_D <ParameterString>
                                                    None,        #INPUT_E <ParameterRaster>
                                                    '1',         #BAND_E <ParameterString>
                                                    None,        #INPUT_F <ParameterRaster>
                                                    '1',         #BAND_F <ParameterString>
                                                    NDVI_syntax, #FORMULA <ParameterString>
                                                    '',          #NO_DATA <ParameterString>
                                                    5,           #RTYPE <ParameterSelection>
                                                    '0',         #EXTRA <ParameterString>
                                                    None)        #OUTPUT <OutputRaster>

NDVI = QgsRasterLayer(outputs_GDALOGRRASTERCALCULATOR_1['OUTPUT'],'NDVI')

QgsMapLayerRegistry.instance().addMapLayer(NDVI)










