import numpy as np
from PIL import Image
from read_tif import read_tif

def filter_progress(input_name,threshold):
    """
    this method generates a black and white image from a input greyscale tif at a given threshold
    pixel values below the threshold are converted to black and values above the threshold are converted to white
    @param:input file path, threshold value (0-255)
    """
    workspace = '/Users/jiaying/Downloads/TDA/data/tif/trump/'
    input_file = workspace+input_name+".tif"

    np_img = read_tif(input_file)

    filtered = np.where(np_img>threshold,255,0)
    output_file = workspace+input_name + "_%d.tif"%threshold
    im = Image.fromarray((filtered).astype(np.uint8))
    im.save(output_file)
