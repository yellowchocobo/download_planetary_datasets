import numpy as np
from pathlib import Path
from datetime import datetime

def floor_nearest(range_l, min_l, max_l):
    """
    This is a quickfix so that if you are interested let's say in having
    latitudes between 82 and 85, it will return automatically the latitudes of
    the mosaics that contain the min and max latitudes (in this case, 80 and
    84, as the product with latitudes 80 and 84 covers --> 80-84 and 84-88).

    Parameters
    ----------
    l: int or float
    longitude or latitude

    Returns
    -------
    Closest value
    """

    idx_min = (np.abs(range_l - min_l)).argmin()
    idx_max = (np.abs(range_l - max_l)).argmin()
    value_min = (range_l[idx_min])
    value_max = (range_l[idx_max])

    if value_min == min_l:
        None
    elif value_min > min_l:
        if idx_min - 1 < 0:
            None
        else:
            value_min = (range_l[idx_min - 1])
    else:
        None

    if value_max == max_l:
        None
    elif value_max < max_l:
        if idx_max + 1 == len(range_l):
            None
        else:
            value_max = (range_l[idx_max + 1])
    else:
        None

    return (value_min, value_max)

def floor_nearest_latitude(min_l, max_l):
    """
    See above.
    """

    range_l = np.arange(-88,90,4)
    return (floor_nearest(range_l, min_l, max_l))

def floor_nearest_longitude(min_l, max_l):
    """
    See above.
    """
    range_l = np.arange(-180,181,4)
    return (floor_nearest(range_l, min_l, max_l))

def get_links(min_latitude, max_latitude, min_longitude, max_longitude,
              output_folder):
    """
    returns all the CTX links within the specified latitudes and longitudes

    Parameters
    ----------
    min_latitude : int (between -90 and +90)
        Minimum latitude to select in degrees
    max_latitude : int (between -90 and +90)
        Maximum latitude to select in degrees
    min_longitude : int (between -180 and 180)
        Minimum longitude in degrees
    max_longitude : int (between -180 and 180)
        Maximum longitude in degrees
    output_folder : str
        folder in which the links to all of the CTX images

    Returns
    -------
    default_link : str
        link to the kaguya's ftp for the corresponding product
    default_link2 : str
        productname
    degrees_per_latlon : int
        width and height of the tile in degrees
    """
    links = []

    ftp = "http://murray-lab.caltech.edu/CTX/tiles/beta01/"
    portion_string1 = "Murray-Lab_CTX-Mosaic_beta01_"
    portion_string3 = "data.zip"
    degrees_per_latlon = 4

    min_longitude, max_longitude = floor_nearest_longitude(min_longitude, max_longitude)
    min_latitude, max_latitude = floor_nearest_longitude(min_latitude,
                                                         max_latitude)

    for i in range(min_longitude, max_longitude, degrees_per_latlon):
        lon = 'E' + str(int(i)).zfill(3)

        for j in range(min_latitude, max_latitude, degrees_per_latlon):
            lat = 'N' + str(int(j)).zfill(2)

            filename = (ftp + lon + "/" + portion_string1 + lon + "_" + lat +
                        "_" + portion_string3)
            links.append(filename)

    # make parent directory if not existing
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # get time
    now = datetime.now()
    dt_string = now.strftime("%m-%d-%Y-%H%M")

    # save to text file
    np.savetxt(output_folder + "CTX_download_" + dt_string + ".txt",
               np.array(links), fmt="%s")

    print('CTX text file is generated')

    return (links)

min_latitude = 78.0
max_latitude = 83.0
min_longitude = -120.0
max_longitude = 120.0

links = get_links(min_latitude, max_latitude,
                  min_longitude, max_longitude,
                  "/home/nilscp/tmp/test_CTX/")