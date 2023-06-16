# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:21:38 2019

@author: nilscp
"""
import glob, os
import numpy as np
import subprocess
import sys
from pathlib import Path

sys.path.append('/home/nilscp/GIT/rastertools')
import utils


def translate(args):
    """with a def you can easily change your subprocess call"""
    # command construction with binary and options
    options = ['/bin/gdal_translate']
    options.extend(args)
    # call gdalwarp
    subprocess.check_call(options)

def EQC_360_to_180_domain(ulx_scy_360, lrx_scy_360, width, cellsize):
    
    ulx_degree = ulx_scy_360 / (width*cellsize)
    lrx_degree = lrx_scy_360 / (width*cellsize)

    # ulx < lrx
    if np.round(ulx_degree) >= 180.0:
        ulx_degree_180 = -(360.0 - ulx_degree)
        lrx_degree_180 = -(360.0 - lrx_degree)
    else:
        ulx_degree_180 = ulx_degree
        lrx_degree_180 = lrx_degree

    ulx_sc180 = ulx_degree_180 * (width*cellsize)
    lrx_sc180 = lrx_degree_180 * (width*cellsize)
    
    return (ulx_sc180, lrx_sc180)


def translate_batch(path_raster):
    # change directory
    os.chdir(path_raster)
    img_list = glob.glob("*.img")
    img_dummy = Path(path_raster) / 'dummy.img'

    for img in img_list:

        try:
            filename_img = img_dummy.with_name(img)
            filename_tif = img_dummy.with_name(img.split(".img")[0] + ".tif")
            filename_lbl = img_dummy.with_name(img.split(".img")[0] + ".lbl")

            translate([filename_lbl, filename_tif])

            # remove files, and rename final tif file
            filename_img.unlink()
            filename_lbl.unlink()

        except:
            None

def DTMMAP_360_to_180_domain(path_raster):
    
    
    # change directory
    os.chdir(path_raster)
    img_list = glob.glob("*.img")
    img_dummy = Path(path_raster) / 'dummy.img'

    for img in img_list:

        try:

            filename_img = img_dummy.with_name(img)
            filename_tif = img_dummy.with_name(img.split(".img")[0] + ".tif")
            filename_lbl = img_dummy.with_name(img.split(".img")[0] + ".lbl")
            filename_tif_shifted = img_dummy.with_name(img.split(".img")[0] + "_shifted.tif")

            translate([filename_lbl, filename_tif])

            meta = utils.get_raster_profile(filename_tif)
            resolution = utils.get_raster_resolution(filename_tif)
            width = meta['width']
            bbox = utils.get_raster_bbox(filename_tif) #xmin, ymin, xmax, ymax

            ulx = bbox[0]
            uly = bbox[-1]
            lrx = bbox[2]
            lry = bbox[1]

            (ulx_sc180, lrx_sc180) = EQC_360_to_180_domain(ulx,
                                                           lrx,
                                                           width,
                                                           cellsize=resolution[0])

            translate(['-a_ullr', str(ulx_sc180), str(uly), str(lrx_sc180),
                       str(lry), filename_tif, filename_tif_shifted])

            # remove files, and rename final tif file
            filename_img.unlink()
            filename_lbl.unlink()
            filename_tif.unlink()
            filename_tif_shifted.rename(filename_tif.as_posix())

        except:
            None