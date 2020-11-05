'''
check http://wms.lroc.asu.edu/lroc/thumbnails
website for more footprint products of NAC & WAC images.

Example
-------  
DTM_footprints = ("/home/nilscp/tmp/NAC_EQ_FOURTH_EXTENDED_SCIENCE_MISSION_360/"
                 "NAC_EQ_FOURTH_EXTENDED_SCIENCE_MISSION_360.SHP")


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
import subprocess
from pathlib import Path

def select(footprints_geopackage,
           footprints,
           range_latitude,
           range_longitude,
           range_incidence = (0.0, 180.0),
           range_emission = (0.0, 90.0),
           range_phase = (0.0, 180.0)):
    
    """
    Select available footprints based on latitude and longitude
    
    Parameters
    ----------
    footprints_geopackage : geopackage containing footprints
        path
    footprints : name of the mission
        str
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
    
    df_DTM_footprints = gpd.read_file(filename=footprints_geopackage, layer=footprints)
    
    # TODO I need to figure why it is not working with the lunar proj. coord
    #df_DTM_footprints.crs = "EPSG:104903"
    
    # selection of latitudes
    lat_selection = np.logical_and(
        df_DTM_footprints.center_lat >= range_latitude[0],
        df_DTM_footprints.center_lat <= range_latitude[1])
    
    
    # selection of longitudes
    lon_selection = np.logical_and(
        df_DTM_footprints.center_lon >= range_longitude[0],
        df_DTM_footprints.center_lon <= range_longitude[1])
    
    # selection of footprints for specified latitudes and longitudes
    latlon_selection = np.logical_and(lat_selection, lon_selection)
    df_latlon_selection = df_DTM_footprints[latlon_selection]
    
    # selection of incidence angles
    inc_selection = np.logical_and(
            df_latlon_selection.inc_angle >= range_incidence[0],
            df_latlon_selection.inc_angle <= range_incidence[1])
    
    # selection of emission angles
    emi_selection = np.logical_and(
            df_latlon_selection.emssn_ang >= range_emission[0],
            df_latlon_selection.emssn_ang <= range_emission[1])
    
    # selection of phase angles
    pha_selection = np.logical_and(
            df_latlon_selection.phase_angl >= range_phase[0],
            df_latlon_selection.phase_angl <= range_phase[1])
    
    # dataframe selection
    selection = np.logical_and(np.logical_and(inc_selection, emi_selection),
                               pha_selection)
                               
    df_selection = df_latlon_selection[selection]
    
    return (df_selection)


def get_url_for_download(output_filename, df_selection):
    '''   

    Parameters
    ----------
    output_filename : output text filename
        path.
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
    df_selection["url_nac"] = ("http://lroc.sese.asu.edu/data/" + 
                               df_selection.file_speci)
    url_nac = df_selection.url_nac
    url_nac.to_csv(output_filename, header=False, index=None, sep=',')
    
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


def download(filename):
    """

    Parameters
    ----------
    filename

    Returns
    -------

    """
    filename_p = Path(filename)

    list_files = subprocess.run(["wget", "-P", filename_p.parent.as_posix(), "-nd", "-i", filename_p.as_posix()])
    print("The exit code was: %d" % list_files.returncode)

    return 0