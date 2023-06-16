from pathlib import Path
import shutil

BASH_SCRIPT_FOLDER = Path("/home/nilscp/GIT/download_planetary_datasets/ISIS3")
NAC_ISIS3_TEMPLATE = BASH_SCRIPT_FOLDER / "NAC-ISIS3-processing.sh"
PROCESSING_BATCH_BASH_SCRIPT = BASH_SCRIPT_FOLDER / "processing_batch_2022.sh"
BATCH_GDAL_SCRIPT = BASH_SCRIPT_FOLDER / "batch-gdal-translate.sh"

def update_download_csv(filename_csv):
    """
    http://pds.lroc.asu.edu/data/LRO-L-LROC-2-EDR-V1.0/LROLRC_0047A/DATA/ESM4/2021076/NAC/M1370656957RE.IMG
    http://pds.lroc.asu.edu/data/LRO-L-LROC-3-CDR-V1.0/LROLRC_1047A/DATA/ESM4/2021076/NAC/M1370656957RC.IMG
    Parameters
    ----------
    filename_csv

    Returns
    -------

    """
    filename_csv = Path(filename_csv)
    with open(filename_csv, "r") as file:
        lines= [line for line in file]
        new_lines = []
        for l in lines:
            if l.endswith("C.IMG\n"):
                new_line = l.replace("LRO-L-LROC-3-CDR-V1.0","LRO-L-LROC-2-EDR-V1.0")
                new_line = new_line.replace(l.split("/")[5][7:11], "0" + l.split("/")[5][8:11])
                new_line = new_line.replace("C.IMG","E.IMG")
                new_lines.append(new_line)
            else:
                new_lines.append(l)

    with open(filename_csv.with_name(filename_csv.name.replace(".csv", "-updated.csv")), "w") as file:
        file.writelines(new_lines)

def generate_scripts(input_folder):
    input_folder = Path(input_folder)
    folders = list(input_folder.glob("*"))

    # to modify
    with open(NAC_ISIS3_TEMPLATE) as file_NAC:
        lines_NAC = [line for line in file_NAC]

    for f in folders:

        # to calculate processing time
        with open(f / (f.name + "-to-download.csv")) as csv_file:
            n = len([line for line in csv_file])
            n = n * 2 # at least two hours of processing per image

        lines_NAC[2] = lines_NAC[2].split("=")[0] + "=" + f.name + "_ISIS3\n"
        lines_NAC[3] = lines_NAC[3].split("=")[0] + "=" + str(n).zfill(2) + ":00:00\n"

        with open(f / ("NAC-ISIS3-processing.sh"), "w") as out_file:
            out_file.writelines(lines_NAC)

        # copy the two other files
        shutil.copy2(PROCESSING_BATCH_BASH_SCRIPT, f / ("processing_batch.sh"))
        shutil.copy2(BATCH_GDAL_SCRIPT, f / ("batch-gdal-translate.sh"))

        # update download file
        update_download_csv(f / (f.name + "-to-download.csv"))


def create_folders(input_folder):
    input_folder = Path(input_folder)
    files = list(input_folder.glob("*.csv"))
    for f in files:
        nf = f.with_name(f.name.split("-")[0])
        nf.mkdir(parents=True, exist_ok=True)
        f.rename(nf / f.name)

def keep_only_tif(input_folder):
    input_folder = Path(input_folder)
    folders = list(input_folder.glob("c*"))

    print("Deleting cub and IMG files...")
    for f in folders:
        cub = list(f.glob("*.cub"))
        img = list(f.glob("*.IMG"))
        for c in cub:
            c.unlink()
        for i in img:
            i.unlink()
    print("Done.")



