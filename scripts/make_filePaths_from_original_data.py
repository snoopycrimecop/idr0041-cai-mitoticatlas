#!/usr/bin/env python
# Generate filePaths tsv file for idr0041 study file
# This script detects the TIFF files under the specified base directory and
# generates a tsv file using the name of the top-level assay folder as the
# target dataset and the name of the cell folder to create the image name

from glob import glob
import logging
import os
from os.path import basename, join
import sys

# Environment variables
BASE_DIRECTORY = os.environ.get(
    "BASE_DIRECTORY", "/uod/idr/filesets/idr0041-cai-mitoticatlas/")
START = int(os.environ.get("START", 1))
if "STOP" in os.environ:
    STOP = int(os.environ.get("STOP"))
else:
    STOP = None
DEBUG = int(os.environ.get("DEBUG", logging.INFO))
IMAGE_TYPES = {
    'raw': 'rawtif',
    'mask': 'masktif',
    'conc': 'conctif',
}
CORRECTION_DIRECTORY = "/nfs/bioimage/drop/idr0041-cai-mitoticatlas/20180710-ftp"

# Initialize logging and perform minimal directory sanity check
logging.basicConfig(level=DEBUG)
if not os.path.exists(BASE_DIRECTORY):
    logging.error("Cannot find the raw data directory. Exiting.")
    sys.exit(0)

# Determine base location for filePaths tsv file
metadata_dir = os.path.dirname(os.path.realpath(__file__))
filepaths_file = join(metadata_dir, "..", "experimentA",
                      "idr0041-experimentA-filePaths.tsv")

# List all original folders found under base directory
original_folders = [join(BASE_DIRECTORY, x) for x in
                    os.listdir(BASE_DIRECTORY)]
original_folders = sorted(filter(os.path.isdir, original_folders))
logging.info("Found %g folders under %s" % (len(original_folders),
             BASE_DIRECTORY))

# List all correction folders
correction_folders = [x for x in os.listdir(CORRECTION_DIRECTORY)]
logging.info("Found %g correction folders under %s" % (len(correction_folders),
             CORRECTION_DIRECTORY))

# Loop over subset of assay folders delimited by START and STOP
files = []
folders = original_folders[START - 1:STOP]
logging.info("Generating %s for %g folders" % (filepaths_file, len(folders)))
for folder in folders:
    logging.debug("Finding cells under %s" % folder)
    # Retrieve individual cell per assays excluding calibration folders
    cells = [x for x in glob(folder + "/*") if not x.endswith("Calibration")]
    for cell in cells:
        for t in IMAGE_TYPES:
            assay = basename(folder) + "_%s" % t

            if assay in correction_folders:
                logging.debug("%s:%s using images from corrected folder",
                              assay, basename(cell))
                subfolder = "%s/%s/%s*" % (
                    CORRECTION_DIRECTORY, assay, basename(cell))
            else:
                subfolder = cell + "/%s/*" % IMAGE_TYPES[t]
            tifs = sorted([x for x in glob(subfolder)
                           if not x.endswith("Thumbs.db")])
            logging.debug("Found %g original files under %s" % (
                          len(tifs), subfolder))

            for tif in tifs:
                imagename = basename(cell) + basename(tif)[-10:-4]
                files.append((assay, tif, imagename))

logging.info("Listed %g files to import" % len(files))

with open(filepaths_file, 'w') as f:
    for i in files:
        f.write("Dataset:name:%s\t%s\t%s\n" % (i[0], i[1], i[2]))
