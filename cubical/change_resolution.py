from matplotlib import image
import json
import numpy as np
from PIL import Image
import scipy.misc
import math
import scipy.stats
from read_tif import read_tif

def change_resolution(seg,px_width,method='mean'):
    """
    this method resolve image(matrix) by a user given pixel width
    @param: matrix, pixel width, method of merging(mean/mdoe)
    """
    new_seg = []
    max_height, max_width = seg.shape
    n_y = math.floor(max_height/px_width)
    n_x = math.floor(max_width/px_width)
    for i in range(n_y):
        for j in range(n_x):
            new_cell = seg[i*px_width:(i+1)*px_width,j*px_width:(j+1)*px_width]
            n_nonzero = np.count_nonzero(new_cell)
            if method == 'mean':
                if (n_nonzero == px_width**2) | (n_nonzero == 0):
                    new_cell = np.mean(new_cell)
                else:
                    masked = np.ma.masked_equal(new_cell, 0)
                    new_cell = np.mean(masked)
            elif method == 'mode':
                temp = np.sort(new_cell.flatten()[::-1])
                mode,count = scipy.stats.mode(temp)
                new_cell =mode[0]
            new_seg.append(int(new_cell))
    new_seg = np.reshape(new_seg,(n_y,n_x))

    #output_file = "/Users/jiaying/Downloads/TDA/data/tif/seg40p_inverse.tif"
    return new_seg

def change_resolution_save(input_file,output_file,px_width,method):
    """
    this method reads image from file and save resolved image as file
    @param: iinput imgae file name, output image name, method of merging(mean/mdoe)
    """
    if method == 'mean':
        np_img = np.loadtxt(input_file)
        seg = change_resolution(np_img,'mean')
        seg = np.where(seg==0,255,seg)
    elif method == 'mode':
        np_img = read_tif(input_file)
        seg = change_resolution(np_img,px_width,'mode')
    im = Image.fromarray((seg).astype(np.uint8))
    im.save(output_file)

if __name__ == '__main__':
    change_resolution_save("/Users/jiaying/Downloads/TDA/data/tif/trump/04.tif",'/Users/jiaying/Downloads/TDA/data/tif/trump/04_8184to1023.tif',8,'mode')
