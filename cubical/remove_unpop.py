import numpy as np
from PIL import Image
from read_tif import read_tif

def remove_unpop(f_pop,f_vote):
    """
    this method removes the unpopulated areas from a voting map
    @param: population data file, voting data file
    """
    #pop = image.imread(f_pop)
    pop = read_tif(f_pop)
    vote = image.imread(f_vote)
    #vals = []
    #for i in range(pop.shape[0]):
    #    for j in range(pop.shape[1]):
    #        if pop[i,j][0] > 0:
    #            vals.append(1)
    #        else:
    #            vals.append(0)
    #pop_matrix = np.reshape(vals,(352,1023))
    pop_matrix = np.where(pop==255,0,1)
    height = 2800
    weight = 8176
    extended_pop = [pop_matrix[math.floor(h/16),math.floor(w/16)] for h in range(height) for w in range(weight)]
    extended_pop = np.reshape(extended_pop,(height,weight))
    #test = np.multiply(pop_matrix[100],vote[100])
    result = np.multiply(extended_pop,vote[:2800,:8176])
    result = np.where(result==0,255,result)

    output_file = "/Users/jiaying/Downloads/TDA/data/tif/trump/virginia8184p_final.tif"
    #output_file = "/Users/jiaying/Downloads/TDA/data/tif/virginia_final_inverse.tif"
    im = Image.fromarray((result).astype(np.uint8))
    im.save(output_file)

    output_txt = "/Users/jiaying/Downloads/TDA/data/tif/trump/virginia8184p_final.txt"
    #output_txt = "/Users/jiaying/Downloads/TDA/data/tif/virginia_final_inverse.txt"
    with open(output_txt,'w') as f:
        temps = []
        for line in result:
            temps.append(' '.join([str(e) for e in line]))
        f.write('\n'.join(temps))
