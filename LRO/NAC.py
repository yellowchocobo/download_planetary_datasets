'''
check http://wms.lroc.asu.edu/lroc/thumbnails
check https://wms.lroc.asu.edu/lroc/rdr_product_select (selecting for shapefiles)
Check RDR products and shapefile products. There, it should be
website for more footprint products of NAC & WAC images.

Right now there is a mix of CDR and EDR in the footprints (which is very annoying!), why are they giving footprints of CDR...

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
from shapely.geometry import box

sys.path.append("/home/nilscp/GIT/rastertools/")
import generalutils
import crs

def select_shapefile(lon_format=360):

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

    if lon_format == 360:
        footprints_p = Path("/home/nilscp/QGIS/Moon/NAC_footprints/NAC_footprints_360.shp")
    else:
        footprints_p = Path("/home/nilscp/QGIS/Moon/NAC_footprints/NAC_footprints_180.shp")

    return footprints_p

def spatial_query(range_latitude, range_longitude, lon_format):
    input_dir = Path("/home/nilscp/QGIS/Moon/NAC_footprints")
    all_gdfs = []
    dir_180 = list(input_dir.glob("NAC*_180"))
    bbox = box(range_longitude[0], range_latitude[0],
               range_longitude[1], range_latitude[1])

    gs_bbox = gpd.GeoSeries(bbox, crs=crs.Moon_2000())

    if lon_format == 180:
        input_dir = list(input_dir.rglob("NAC*_180"))
    else:
        input_dir = list(input_dir.rglob("NAC*_360"))

    all_gdfs = []
    for d in input_dir:
        # get crs without opening the file
        if d.name.split("_")[1] == "SP":
            shp_crs = crs.Moon_South_Pole_Stereographic()
        elif d.name.split("_")[1] == "NP":
            shp_crs = crs.Moon_North_Pole_Stereographic()
        else:
            shp_crs = crs.Moon_2000()

        gs_bbox_proj = gs_bbox.to_crs(shp_crs)

        gdf = gpd.read_file(list(d.glob("*.SHP"))[0], bbox=gs_bbox_proj)

        if lon_format == 180:
            gdf_proj = gdf.to_crs(crs.Moon_Equirectangular())
        else:
            gdf_proj = gdf.to_crs(crs.Moon_Equirectangular_360())
        all_gdfs.append(gdf_proj)

    gdf_boulders = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True))
    return gdf_boulders

def id_query(gdf, id):
    # single query (e.g., one id -> 'M139694087LE' or pair of id ->'M139694087')
    if type(id) == str:
        gdf_selection = gdf[gdf.product_id.str.startswith(id)]
    # or multiple queries -> ['M139694087LE', 'M139694087RE']
    else:
        gdf_selection = gdf[gdf['product_id'].isin(id)]
    return gdf_selection


def filter_query(gdf_footprints,
                 max_resolution= 9999.0,
                 range_incidence = (0.0, 180.0),
                 range_emission = (0.0, 90.0),
                 range_phase = (0.0, 180.0)):
    
    """
    Select available footprints based on latitude and longitude
    
    Parameters
    ----------
    geopackage : Path
        geopackage containing footprint layers
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
    # selection of resolution
    gdf_footprints = gdf_footprints[gdf_footprints.RESOLUTION < max_resolution]

    # selection of incidence angles
    inc_selection = np.logical_and(
            gdf_footprints.INC_ANGLE >= range_incidence[0],
            gdf_footprints.INC_ANGLE <= range_incidence[1])

    # selection of emission angles
    emi_selection = np.logical_and(
            gdf_footprints.EMSSN_ANG >= range_emission[0],
            gdf_footprints.EMSSN_ANG <= range_emission[1])

    # selection of phase angles
    pha_selection = np.logical_and(
            gdf_footprints.PHASE_ANGL >= range_phase[0],
            gdf_footprints.PHASE_ANGL <= range_phase[1])

    # dataframe selection
    selection = np.logical_and(np.logical_and(inc_selection, emi_selection),
                               pha_selection)

    gdf_selection = gdf_footprints[selection]

    return (gdf_selection)


def get_url_for_download(gdf_selection, output_filename, output_dir='.'):
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
                               gdf_selection.FILE_SPECI)
    url_nac = gdf_selection.url_nac
    url_nac.to_csv(outfile, header=False, index=None, sep=',')

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

def create_map_projection(lat, lon, proj_name='projection', output_dir='.'):

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

    outfile = apath / (proj_name + '.map')

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