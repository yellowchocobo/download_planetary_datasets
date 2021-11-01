'''
check http://wms.lroc.asu.edu/lroc/thumbnails
Check RDR products and shapefile products. There, it should be
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

import pandas as pd
import geopandas as gpd
import numpy as np
import subprocess
import sys
from pathlib import Path

sys.path.append("/home/nilscp/GIT/rastertools/")
import generalutils

def select_geopackage(range_latitude, lon_format=360):

    """

    Parameters
    ----------
    range_latitude : tuple of float or int (lat_min, lat_max)
        range of possible values, -90 to 90.
    lon_format: int
        format of longitude: 180 (-180-180) or 360 (0-360)

    Returns
    -------
    Path to footprint geopackage
    """

    footprints_geopackage = Path("/home/nilscp/Downloads/NAC_footprints/geopackage")

    # Equatorial
    if np.logical_and(min(range_latitude) > -60.0, max(range_latitude) < 60.0):
        if lon_format == 360:
            geopackage = footprints_geopackage.with_name("NAC_footprints_EQ360.gpkg")
        else:
            geopackage = footprints_geopackage.with_name("NAC_footprints_EQ180.gpkg")

    # North pole
    if min(range_latitude) > 60.0:
        if lon_format == 360:
            geopackage = footprints_geopackage.with_name("NAC_footprints_NP360.gpkg")
        else:
            geopackage = footprints_geopackage.with_name("NAC_footprints_NP180.gpkg")

    # South pole
    if max(range_latitude) < -60.0:
        if lon_format == 360:
            geopackage = footprints_geopackage.with_name("NAC_footprints_SP360.gpkg")
        else:
            geopackage = footprints_geopackage.with_name("NAC_footprints_SP180.gpkg")

    return geopackage

def select_footprints(geopackage,
                      range_latitude,
                      range_longitude,
                      range_incidence = (0.0, 180.0),
                      range_emission = (0.0, 90.0),
                      range_phase = (0.0, 180.0)):

    """
    TODO: It would have been better to save the results of this function for EQ, NP and SP to a sql database. For
    now, I am filtering every layer to avoid to load 1 million footprints, a process which takes quite lot of time.

    Parameters
    ----------
    geopackage

    Returns
    -------

    """

    layers = generalutils.listLayers(geopackage)
    gdfs_list = []
    for i, layer in enumerate(layers):
        gdfs_list.append(filter_footprints(geopackage,
                                           layer,
                                           range_latitude,
                                           range_longitude,
                                           range_incidence,
                                           range_emission,
                                           range_phase))

    gdfs = gpd.GeoDataFrame(pd.concat(gdfs_list, ignore_index=True), crs=gdfs_list[0].crs)

    return gdfs



def filter_footprints(geopackage,
                      layer,
                      range_latitude,
                      range_longitude,
                      range_incidence = (0.0, 180.0),
                      range_emission = (0.0, 90.0),
                      range_phase = (0.0, 180.0)):
    
    """
    Select available footprints based on latitude and longitude
    
    Parameters
    ----------
    geopackage : Path
        geopackage containing footprint layers
    layer : layer in geopackage
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
    gdf_selection : GeoPandas dataframe
        GeoPandas dataframe based on specified latitude, longitude, incidence, emission and phase
    """
    gdf_footprints = gpd.read_file(filename=geopackage, layer=layer)

    # TODO I need to figure why it is not working with the lunar proj. coord
    #gdf_footprints.crs = "EPSG:104903"
    
    # selection of latitudes
    lat_selection = np.logical_and(
        gdf_footprints.center_lat >= range_latitude[0],
        gdf_footprints.center_lat <= range_latitude[1])
    
    
    # selection of longitudes
    lon_selection = np.logical_and(
        gdf_footprints.center_lon >= range_longitude[0],
        gdf_footprints.center_lon <= range_longitude[1])
    
    # selection of footprints for specified latitudes and longitudes
    latlon_selection = np.logical_and(lat_selection, lon_selection)
    gdf_latlon_selection = gdf_footprints[latlon_selection]
    
    # selection of incidence angles
    inc_selection = np.logical_and(
            gdf_latlon_selection.inc_angle >= range_incidence[0],
            gdf_latlon_selection.inc_angle <= range_incidence[1])
    
    # selection of emission angles
    emi_selection = np.logical_and(
            gdf_latlon_selection.emssn_ang >= range_emission[0],
            gdf_latlon_selection.emssn_ang <= range_emission[1])
    
    # selection of phase angles
    pha_selection = np.logical_and(
            gdf_latlon_selection.phase_angl >= range_phase[0],
            gdf_latlon_selection.phase_angl <= range_phase[1])
    
    # dataframe selection
    selection = np.logical_and(np.logical_and(inc_selection, emi_selection),
                               pha_selection)
                               
    gdf_selection = gdf_latlon_selection[selection]
    
    return (gdf_selection)


def get_url_for_download(output_filename, gdf_selection, output_dir='.'):
    '''   

    Parameters
    ----------

    output_filename : output text filename ('*.csv')
        path.
    gdf_selection : GeoPandas DataFrame
        DESCRIPTION.
    output_dir : output directory.
        str

    Returns
    -------
    None.
    
    Example
    -------
    # if you want to download the urls
    # write in your terminal
    wget -nc -i <text_file_containing_urls_to_download>

    '''
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    apath = path.absolute()

    outfile = apath / output_filename

    gdf_selection["url_nac"] = ("http://lroc.sese.asu.edu/data/" +
                               gdf_selection.file_speci)
    url_nac = gdf_selection.url_nac
    url_nac.to_csv(outfile, header=False, index=None, sep=',')
    
def to_shp(output_filename, gdf_selection, output_dir='.'):
    '''

    Parameters
    ----------
    output_filename : str
        absolute path to filename
    gdf_selection : GeoPandas DataFrame
        DESCRIPTION.
    output_dir: str
        Absolute or relative output dir

    Returns
    -------
    None.

    '''
    path = Path(output_dir)
    apath = path.absolute()

    if "shp" in output_filename:
        outfile = apath / output_filename
        gdf_selection.to_file(outfile, driver = 'ESRI Shapefile')
        print ("Shapefile " + outfile.as_posix() + " has been generated")

    elif "gpkg" in output_filename:
        geopackage, layer = output_filename.split(',')
        outfile = apath / geopackage
        gdf_selection.to_file(outfile, layer=layer, driver='GPKG')
        print("Layer " + layer + " has been generated in geopackage " + outfile.as_posix())

    else:
        print ("the specified format is not recognized")
    

# TODO
# overlap of a polygon shapefile with footprint
# or get max boundary from shapefiles and feed it in the selection.
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

#TODO

def create_map_projection(lat, lon, product_id='projection', output_dir='.'):

    """

    Parameters
    ----------
    lat
    lon
    product_id
    output_dir

    Returns
    -------

    """

    path = Path(output_dir)
    apath = path.absolute()

    outfile = apath / (product_id + '.map')

    print("creating .map projection file " + outfile.as_posix() + " ...")

    with open(outfile, 'w+') as f:
        f.write('Group = Mapping\n')
        f.write('    ProjectionName  = EQUIRECTANGULAR\n')
        f.write('    CenterLongitude = ' + str(np.round(lon, decimals=2)) + '\n')
        f.write('    CenterLatitude = ' + str(np.round(lat, decimals=2)) + '\n')
        f.write('End_Group\n')
        f.write('End')

def map_projection_ISIS3(gdf_selection, common_projection=False, output_dir='.'):

    """
    To finish

    Generate the projection

    Parameters
    ----------
    gdf_selection
    common_projection

    Returns
    -------

    Example:

    Group = Mapping
        ProjectionName  = EQUIRECTANGULAR
        CenterLongitude = 0.0
        CenterLatitude = 0.0
    End_Group
    End


    """
    if common_projection:
        lat = np.round(np.average(gdf_selection.center_lat.values), decimals=2)
        lon = np.round(np.average(gdf_selection.center_lon.values), decimals=2)

        create_map_projection(lat, lon, product_id='projection', output_dir=output_dir)
    else:
        for i in range(gdf_selection.shape[0]):
            create_map_projection(gdf_selection.center_lat.iloc[i],
                                  gdf_selection.center_lon.iloc[i],
                                  product_id=gdf_selection.product_id.iloc[i],
                                  output_dir=output_dir)