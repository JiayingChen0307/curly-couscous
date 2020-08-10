from read_tif import read_tif
import numpy as np
from PIL import Image

def gen_random_proportion(input_name):
    """
    this method generates a random graph with the same number of dark(<128), light(>128) and unpop (=255) as a given graph
    @param: name of the input file (e.g.12_8184)
    """
    np_img = read_tif("/Users/jiaying/Downloads/TDA/cubical/8184p/%s.tif"%input_name)
    h,w = np_img.shape

    #light_num  = (np_img>128).sum() - (np_img==255).sum()
    #dark_arr = np.random.randint(128,size=(np_img<128).sum())
    #light_arr = np.random.randint(1,128,size=light_num)+128
    #unpop_arr = np.full((np_img==255).sum(),255)
    #dark_arr = np.random.randint(128,size=(np_img<128).sum())
    #light_arr = np.random.randint(128,size=light_num)+128
    #unpop_arr = np.full((np_img==255).sum(),255)

    #if (np_img==128).sum() != 0:
    #    equal_arr =  np.full((np_img==128).sum(),128)
    #    result = np.concatenate((dark_arr,light_arr,unpop_arr,equal_arr))
    #else:
    #    result = np.concatenate((dark_arr,light_arr,unpop_arr))
    result = np_img.flatten()
    np.random.shuffle(result)
    result = result.reshape(h,w)
    output_file = "/Users/jiaying/Downloads/TDA/cubical/random/shuffle%s.tif"%input_name
    im = Image.fromarray((result).astype(np.uint8))
    im.save(output_file)
