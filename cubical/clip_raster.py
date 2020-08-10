import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from rasterio import features
from shapely.geometry import box
import geopandas as gpd
import fiona
from fiona.crs import from_epsg
import pycrs
import json
from matplotlib import image
import json
import numpy as np
from PIL import Image
import scipy.misc
import math

def clip_raster(mask_from_file,raster_path, out_tif):
    """
    this method clip a raster file from a polygon file, and save it as a new raster file
    @param: polygon filename, raster file, output filename
    """
    data = rasterio.open(raster_path)
    #with fiona.open(polygon_path, "r") as shapefile:
    #    shapes = [feature["geometry"] for feature in shapefile]
    shapes = read_shape(mask_from_file)

    with rasterio.open(raster_path) as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    with rasterio.open(out_tif, "w", **out_meta) as dest:
        dest.write(out_image)

def read_shape(from_file=False):
    """
    this method reads a shapefile and return a list of shapes
    @param: from_file(boolean)
    """
    if from_file:
        polygon_path = '/Users/jiaying/Downloads/TDA/data/VA-shapefiles-master/va_state_dissolve.shp'
        #polygon_path = "/Users/jiaying/Downloads/TDA/data/tif/virginia_beach_dissolve.geojson"
        with fiona.open(polygon_path, "r") as shapefile:
            shapes = [feature["geometry"] for feature in shapefile]
    else:
        shapes = [raster2vector()]

    return shapes

#this method is unused for the poject
def raster2vector():
    out_tif = "/Users/jiaying/Downloads/TDA/data/tif/virginia_beach_pop.tif"
    geojson_template = "/Users/jiaying/Downloads/TDA/geojson_template.geojson"
    with rasterio.open(out_tif) as src:
        grey = src.read(1)
        mask = None
        shapes = features.shapes(grey, mask=mask,transform=src.transform)
        temp = next(shapes)[0]
        print(temp)
    with open(geojson_template) as j:
        data = json.load(j)
        data['features'][0]['geometry'] = temp
    with open("/Users/jiaying/Downloads/TDA/raster2vector_test.geojson",'w') as f:
        json.dump(data,f)
    return temp

def get_va_raster_segment():

    """
    this method crop a segment of the entire virginia tif with given dimension
    """
    input_file = "/Users/jiaying/Downloads/TDA/data/tif/trump/12.tif"
    va_matrix = read_tif(input_file)

    #change the upper and lower bound
    seg = va_matrix[1000:,:500]

    output_file = "/Users/jiaying/Downloads/TDA/data/tif/trump/test.tif"
    im = Image.fromarray((seg).astype(np.uint8))
    im.save(output_file)

def divide_va_raster(n_y,n_x,from_tif=False):
    """
    this method generates a black and white image from a input greyscale tif at a given threshold
    pixel values below the threshold are converted to black and values above the threshold are converted to white
    @param:input file path, threshold value (0-255)
    """
    if from_tif:
        #input = "/Users/jiaying/Downloads/TDA/data/tif/virginia_final_inverse.tif"
        #input = "/Users/jiaying/Downloads/TDA/data/tif/trump/virginia1023p.tif"
        input = "/Users/jiaying/Downloads/TDA/cubical/8184p/virginia8184p.tif"
        va_matrix = read_tif(input)
    else:
        input = "/Users/jiaying/Downloads/TDA/data/tif/virginia_final.txt"
        va_matrix = np.loadtxt(input)

    max_height,max_width = va_matrix.shape
    height = math.floor(max_height/n_y)
    width = math.floor(max_width/n_x)
    for i in range(n_y):
        for j in range(n_x):
            output_file = "/Users/jiaying/Downloads/TDA/cubical/8184p/%d%d_8184.tif"%(i,j)
            seg = va_matrix[i*height:(i+1)*height,j*width:(j+1)*width]
            if not from_tif:
                seg = change_resolution(seg)
                seg = np.where(seg==0,255,seg)
            im = Image.fromarray((seg).astype(np.uint8))
            im.save(output_file)


fp = "/Users/jiaying/Downloads/DATA440/project/usgrid_data_2010/geotiff/uspop10.tif"
fp_final = "/Users/jiaying/Downloads/TDA/data/tif/trump/virginia_beach_epsg4326.tif"
out_tif = "/Users/jiaying/Downloads/TDA/data/tif/virginia_beach_pop.tif"
out_tif_final = "/Users/jiaying/Downloads/TDA/data/tif/virginia_beach_final.tif"
f_vote = "/Users/jiaying/Downloads/TDA/data/tif/trump/virginia1023p.tif"
out_tif = "/Users/jiaying/Downloads/TDA/data/tif/virginia_pop.tif"
#clip_raster(True,fp,out_tif)
#gen_random_proportion('12_8184to256')
#remove_unpop('/Users/jiaying/Downloads/TDA/data/tif/virginia511p_final_inverse.tif', "/Users/jiaying/Downloads/TDA/data/tif/trump/virginia8184p.tif")
#get_va_raster_segment()
#new_arr = change_resolution(arr)
#output_files = ["/Users/jiaying/Downloads/TDA/data/tif/random.tif","/Users/jiaying/Downloads/TDA/data/tif/random_resolve.tif"]
#for i in range(2):
#    im = Image.fromarray((arrs[i]).astype(np.uint8))
#    im.save(output_files[i])
#filter_progress('14',128)
#divide_va_raster(2,6,True)
gen_random_proportion('12_8184')
#dark = np.random.randint(128,size=3697)
#light = np.random.randint(128,size=3698)+128
#result = np.concatenate((light,dark))
#np.random.shuffle(result)
#result = np.reshape(result,(87,85))
#im = Image.fromarray((result).astype(np.uint8))
#im.save('/Users/jiaying/Downloads/TDA/data/tif/random_equal.tif')
