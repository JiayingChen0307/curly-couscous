import numpy as np
from PIL import Image

def read_tif(input_file):
    """
    this method reads a greyscale tif file and return a matrix
    @param: input file path
    """
    # Open the tiff image
    pil_img = Image.open(input_file)

    # Map PIL mode to numpy dtype (note this may need to be extended)
    dtype = {'F': np.float32, 'L': np.uint8}[pil_img.mode]

    # Load the data into a flat numpy array and reshape
    np_img = np.array(pil_img.getdata(), dtype=dtype)
    w, h = pil_img.size
    np_img.shape = (h, w)

    return np_img
