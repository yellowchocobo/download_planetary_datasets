"""
product DTM_MAP_01, SLDEM2013 (1x1 degree):
    default_link = 'http://darts.isas.jaxa.jp/pub/pds3/sln-l-tc-5-sldem2013-v1.0/' 
    default_link2 = '/data/DTM_MAP_01_'
    degrees_per_latlon = 1
    
product TCO_MAP_02, visible orthoimages (3x3 degrees): 
    default_link = 'http://darts.isas.jaxa.jp/pub/pds3/sln-l-tc-5-ortho-map-v2.0/' 
    default_link2 = '/data/TCO_MAP_02_'
    degrees_per_latlon = 3
    
product TCO_MAPe04, visible evening images (3x3 degrees):
    default_link = 'http://darts.isas.jaxa.jp/pub/pds3/sln-l-tc-5-evening-map-v4.0/' 
    default_link2 = '/data/TCO_MAPe04_' # evening
    degrees_per_latlon = 3
    
product TCO_MAPm04, visible morning images (3x3 degrees):
    default_link = 'http://darts.isas.jaxa.jp/pub/pds3/sln-l-tc-5-morning-map-v4.0/' 
    default_link2 = '/data/TCO_MAPm04_' # morning
    degrees_per_latlon = 3
    

Example
-------   
# Download SLDEM2013 in between 40 and 50 N latitudes and 10 and 20 E longitude
get_links_for_download("/home/nilscp/", "DTM_MAP_01", 40, 50, 10, 20)
"""

import numpy as np

'''
**************************************************************************************************
'''

def get_main_repo_links(product_name):
    
    """
    returns the main repository links associated with the specified Kaguya's 
    product and the extent (width/height) of the tile (in degree)
    
    Parameters
    ----------
    product_name : str
        Kaguya's product name 'DTM_MAP_01', 'TCO_MAP_02', 'TCO_MAPe04' or 
        'TCO_MAPm04'
    
    Returns
    -------
    default_link : str
        link to the kaguya's ftp for the corresponding product
    default_link2 : str
        productname
    degrees_per_latlon : int
        width and height of the tile in degrees
    """
    
    kaguya_repo = "http://darts.isas.jaxa.jp/pub/pds3/"
    
    
    try:    
        if product_name == "DTM_MAP_01":
            default_link = kaguya_repo + 'sln-l-tc-5-sldem2013-v1.0/'
            default_link2 = '/data/DTM_MAP_01_'
            degrees_per_latlon = 1
            
        elif product_name == "TCO_MAP_02":
            default_link = kaguya_repo + 'sln-l-tc-5-ortho-map-v2.0/'
            default_link2 = '/data/TCO_MAP_02_'
            degrees_per_latlon = 3
            
        elif product_name == "TCO_MAPe04":
            default_link = kaguya_repo + 'sln-l-tc-5-evening-map-v4.0/'
            default_link2 = '/data/TCO_MAPe04_'
            degrees_per_latlon = 3
            
        elif product_name == "TCO_MAPm04":
            default_link = kaguya_repo + 'sln-l-tc-5-morning-map-v4.0/'
            default_link2 = '/data/TCO_MAPm04_'
            degrees_per_latlon = 3
            
        return (default_link, default_link2, degrees_per_latlon)
            
    except:
        print ("specified KAGUYA's PRODUCT NAME DOES NOT EXIST, please choose"
               " from 'DTM_MAP_01', 'TCO_MAP_02', 'TCO_MAPe04' or 'TCO_MAPm04'")
        
    
def get_links_for_download(output_folder, 
                           product_name, 
                           min_latitude, 
                           max_latitude, 
                           min_longitude, 
                           max_longitude):
    
    """
    returns all the ftp links associated with the specified Kaguya's product 
    within the specified min/max longitudes and latitudes. All the links are
    saved to a text file name '<product_name>_download.txt'
    
    Parameters
    ----------
    output_folder : str
        Name of output folder where the txt file will be saved to
    product_name : str
        Kaguya's product name 'DTM_MAP_01', 'TCO_MAP_02', 'TCO_MAPe04' or 
        'TCO_MAPm04'
    min_latitude : int (between -90 and +90)
        Minimum latitude to select in degrees 
    max_latitude : int (between -90 and +90)
        Maximum latitude to select in degrees 
    min_longitude : int (between 0 and 360)
        Minimum longitude in degrees 
    max_longitude : int (between 0 and 360)
        Maximum longitude in degrees 
    
    Returns
    -------
    default_link : str
        link to the kaguya's ftp for the corresponding product
    default_link2 : str
        productname
    degrees_per_latlon : int
        width and height of the tile in degrees
    """
    
    img_to_download = []
    lbl_to_download = []
    
    # get the strings of the main ftp repository according to the wanted
    # product (as well as the width and height of each tile)
    (default_link, default_link2, degrees_per_latlon) = (
        get_main_repo_links(product_name))

    for i in range(min_longitude, max_longitude, degrees_per_latlon):

        lon1 = 'lon' + str(int(i)).zfill(3)
        lon2 = 'E' + str(int(i)).zfill(3)

        if i + degrees_per_latlon == 360:
            # lon3 = 'E' + str(int(0)).zfill(3) # for DTM_MAP
            lon3 = 'E' + str(int(i + degrees_per_latlon)).zfill(3)
        else:
            lon3 = 'E' + str(int(i + degrees_per_latlon)).zfill(3)

        '''
        Must modify if we want data all the way up to 90 degrees
        '''

        for j in range(min_latitude, max_latitude, degrees_per_latlon):

            if j < -degrees_per_latlon:
                lat1 = 'S' + str(int(abs(j + degrees_per_latlon))).zfill(2)
                lat2 = 'S' + str(int(abs(j))).zfill(2)

            elif j == -degrees_per_latlon:
                lat1 = 'N' + str(int(abs(j + degrees_per_latlon))).zfill(2)
                lat2 = 'S' + str(int(abs(j))).zfill(2)

            else:
                lat1 = 'N' + str(int(abs(j + degrees_per_latlon))).zfill(2)
                lat2 = 'N' + str(int(abs(j))).zfill(2)

            # do
            img_to_download.append(default_link + lon1 + default_link2 + 
                                   lat1 + lon2 + lat2 + lon3 + 'SC.img')            
            
            lbl_to_download.append(default_link + lon1 + default_link2 + 
                                   lat1 + lon2 + lat2 + lon3 + 'SC.lbl')
            
            
    np.savetxt(output_folder + product_name + '_download.txt', 
               np.array(img_to_download + lbl_to_download), fmt="%s")
    
    print ('DONE')