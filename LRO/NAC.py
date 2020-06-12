'''
check http://wms.lroc.asu.edu/lroc/rdr_product_select?commit=Search&filter%5Beast%5D=&filter%5Bgroup_type%5D%5B%5D=Global+Product&filter%5Blat%5D=&filter%5Blon%5D=&filter%5Bnorth%5D=&filter%5Bprefix%5D%5B%5D=&filter%5Brad%5D=&filter%5Bsouth%5D=&filter%5Btext%5D=&filter%5Btopographic%5D=either&filter%5Bwest%5D=&page=2&per_page=10&show_thumbs=1&sort=time_reverse
website for footprint products of NAC & WAC images



Example
-------  
DTM_footprints = "/home/nilscp/tmp/NAC_EQ_FOURTH_EXTENDED_SCIENCE_MISSION_360/NAC_EQ_FOURTH_EXTENDED_SCIENCE_MISSION_360.SHP"


df_selection = select(DTM_footprints,
           range_latitude = (20,30),
           range_longitude = (20,40))

df_selection2 = select(DTM_footprints,
           range_latitude = (20,30),
           range_longitude = (20,40),
           range_incidence = (40, 60),
           range_emission = (0, 15),
           range_phase = (40, 50))

to_shp("/home/nilscp/tmp/NAC_EQ_FOURTH_EXTENDED_SCIENCE_MISSION_360/test1.shp", 
       df_selection)

to_shp("/home/nilscp/tmp/NAC_EQ_FOURTH_EXTENDED_SCIENCE_MISSION_360/test2.shp", 
       df_selection2)
'''

import geopandas as gpd
import numpy as np




def select(footprints_of_LRO_product,
           range_latitude,
           range_longitude,
           range_incidence = (0.0, 180.0),
           range_emission = (0.0, 90.0),
           range_phase = (0.0, 180.0)):
    
    """
    Select available footprints based on latitude and longitude
    
    Parameters
    ----------
    footprints_of_LRO_product : shapefile (*.shp) of footprints
        xxxxxx
    range_latitude : tuple of float or int (lat_min, lat_max)
        range of possible values, -90 to 90.
    range_longitude : tuple of float or int (lon_min, lon_max)
        range of possible values, 0 to 360.
    range_incidence : optional, tuple of float or int  (inc_min, inc_max)
        range of possible values, 0 to 180.
    range_emission : optional, tuple of float or int (emi_min, emi_max)
        range of possible values, 0 to 90.
    range_phase : optional, tuple of float or int (pha_min, pha_max)
        xrange of possible values, 0 to 180.
    
    Returns
    -------
    default_link : str
        link to the kaguya's ftp for the corresponding product
    default_link2 : str
        productname
    degrees_per_latlon : int
        width and height of the tile in degrees
    """
    
    df_DTM_footprints = gpd.read_file(footprints_of_LRO_product)
    
    # TODO I need to figure why it is not working with the lunar proj. coord
    #df_DTM_footprints.crs = "EPSG:104903"
    
    # selection of latitudes
    lat_selection = np.logical_and(
        df_DTM_footprints.CENTER_LAT >= range_latitude[0], 
        df_DTM_footprints.CENTER_LAT <= range_latitude[1])
    
    
    # selection of longitudes
    lon_selection = np.logical_and(
        df_DTM_footprints.CENTER_LON >= range_longitude[0], 
        df_DTM_footprints.CENTER_LON <= range_longitude[1])
    
    # selection of footprints for specified latitudes and longitudes
    latlon_selection = np.logical_and(lat_selection, lon_selection)
    df_latlon_selection = df_DTM_footprints[latlon_selection]
    
    # selection of incidence angles
    inc_selection = np.logical_and(
            df_latlon_selection.INC_ANGLE >= range_incidence[0], 
            df_latlon_selection.INC_ANGLE <= range_incidence[1])
    
    # selection of emission angles
    emi_selection = np.logical_and(
            df_latlon_selection.EMSSN_ANG >= range_emission[0], 
            df_latlon_selection.EMSSN_ANG <= range_emission[1])
    
    # selection of phase angles
    pha_selection = np.logical_and(
            df_latlon_selection.PHASE_ANGL >= range_phase[0], 
            df_latlon_selection.PHASE_ANGL <= range_phase[1])    
    
    # dataframe selection
    selection = np.logical_and(np.logical_and(inc_selection, emi_selection),
                               pha_selection)
                               
    df_selection = df_latlon_selection[selection]
    
    return (df_selection)


def get_url_for_download(output_name, df_selection):
    '''   

    Parameters
    ----------
    df_selection : GeoPandas DataFrame
        DESCRIPTION.

    Returns
    -------
    None.
    
    Example
    -------
    # if you want to download the urls
    # write in your terminal
    wget -nc -i <text_file_containing_urls_to_download>

    '''    
    df_selection["url_nac"] = "http://lroc.sese.asu.edu/data/" + df_selection.FILE_SPECI
    url_nac = df_selection.url_nac
    url_nac.to_csv(output_name, header=None, index=None, sep=',')
    
def to_shp(output_name, df_selection):
    '''

    Parameters
    ----------
    output_name : str
        absolute path to filename
    df_selection : GeoPandas DataFrame
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    df_selection.to_file(output_name, driver = 'ESRI Shapefile')
    print ("Shapefile " + output_name + " has been generated")
    

# TODO
# overlap of a polygon shapefile with footprint     
def overlap():
    None