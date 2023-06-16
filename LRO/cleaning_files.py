from pathlib import Path

def cleaning(input_folder):
    """
    This cleaning function will only keep the tif file (if a tif is detected).

    Parameters
    ----------
    input_folder

    Returns
    -------

    """
    input_folder = Path(input_folder)
    imgs = list(input_folder.rglob("*.IMG"))

    for img in imgs:
        tif = img.with_suffix('.tif')
        if tif.exists():
            img.unlink() # delete img if tif exists

            # delete cub files too
            cubs = list(img.parent.glob(img.stem + "*.cub"))
            for cub in cubs:
                cub.unlink()
        else:
            None

def cleaning_continuously(input_folder):
    """
    This cleaning function will only keep the tif file (if a tif is detected).

    Parameters
    ----------
    input_folder

    Returns
    -------

    """
    input_folder = Path(input_folder)
    imgs = list(input_folder.rglob("*.IMG"))

    for img in imgs:
        cubeatt = img.with_name(img.stem + ".cubeatt.map.cub")
        if cubeatt.exists():
            # delete other cub files (except cubeatt)
            cubs = list(img.parent.glob(img.stem + "*.cub"))
            cubs_del = [c for c in cubs if c != cubeatt]
            for cub in cubs_del:
                cub.unlink()
        else:
            None