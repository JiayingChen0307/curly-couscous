import gdal
from osgeo import ogr, osr
import numpy as np
import matplotlib.pyplot as plt
import time
import logging

def rasterize_shp(county, candidate, max_pixels):
    shp = '/Users/jiaying/Downloads/TDA/data/va_county_shapefiles/' + county + '.shp'

    source_ds = gdal.OpenEx(shp, gdal.OF_VECTOR | gdal.OF_UPDATE)
    source_ds.ExecuteSQL("ALTER TABLE "+county+" DROP COLUMN isHill")

    source_ds = None

    source_ds = ogr.Open(shp, 1)
    source_layer = source_ds.GetLayer()

    fd = ogr.FieldDefn('isHill', ogr.OFTInteger)
    source_layer.CreateField(fd)
    
    for feat in source_layer:
        hillary = float(feat.GetField('G16DPRS'))
        trump = float(feat.GetField('G16RPRS'))
        hill_pct = float((hillary-trump)/(hillary+ trump))
        #if candidate == 'hillary':
        #    hill_grade = float(hill_pct*5)+1
        #elif candidate == 'trump':
        #    hill_grade = float(-hill_pct*5)+1
        feat.SetField('isHill', 128 + 127*hill_pct)
        source_layer.SetFeature(feat)

    x_min, x_max, y_min, y_max = source_layer.GetExtent()
    max_cols = max_rows = max_pixels
    max_pixel_width = (x_max - x_min) / max_cols
    max_pixel_height = (y_max - y_min) / max_rows
    pixel_width = pixel_height = max(max_pixel_width, max_pixel_height)
    cols = int((x_max - x_min) / pixel_height)
    rows = int((y_max - y_min) / pixel_width)

    out_tiff = '/Users/jiaying/Downloads/TDA/data/tif/' + candidate + '/' + county + '.tif'

    target_ds = gdal.GetDriverByName('Gtiff').Create(out_tiff, cols, rows, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_max, 0, -pixel_height))
    band = target_ds.GetRasterBand(1)
    no_data_value = 0
    band.SetNoDataValue(no_data_value)
    band.FlushCache()

    gdal.RasterizeLayer(target_ds, [1], source_layer, options=["ATTRIBUTE=isHill"])
    target_ds_srs = osr.SpatialReference()
    target_ds_srs.ImportFromEPSG(4326)
    target_ds.SetProjection(target_ds_srs.ExportToWkt())

    source_ds = None

    source_ds = gdal.OpenEx(shp, gdal.OF_VECTOR | gdal.OF_UPDATE)
    source_ds.ExecuteSQL("ALTER TABLE "+county+" DROP COLUMN isHill")

    source_ds = None

def main():
    #logging.basicConfig(filename='../logs/ls.log', filemode='w+', level=logging.WARNING)
    #timing_csv = '../runtimes/ls_times.csv'
    #with open(timing_csv,'w+') as timing_file:
        #with open('../full-list') as county_file:
        county_file = ['Virginia Beach']
        for county in county_file:
        # for county in ['003-alpine']:
            #county = county.split('\n')[0]
            for candidate in ['trump']:
                start_time = time.time()
                build_levelset_complex(county, candidate, False, False)
                #timing_file.write(county + ',ls,'+candidate+','+str(time.time()-start_time)+'\n')



rasterize_shp('Virginia Beach','trump', 250)