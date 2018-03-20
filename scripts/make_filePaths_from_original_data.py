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
DEBUG = os.environ.get("DEBUG", logging.INFO)
IMAGE_TYPES = {
    'raw': 'rawtif',
    'mask': 'masktif',
    'conc': 'conctif',
}

# Initialize logging and perform minimal directory sanity check
logging.basicConfig(level=DEBUG)
if not os.path.exists(BASE_DIRECTORY):
    logging.error("Cannot find the raw data directory. Exiting.")
    sys.exit(0)

# Determine base location for filePaths tsv file
metadata_dir = os.path.dirname(os.path.realpath(__file__))
filepaths_file = join(metadata_dir, "..", "experimentA",
                      "idr0041-experimentA-filePaths.tsv")

# Delete tsv file to prevent appending
if os.path.exists(filepaths_file):
    logging.info("Deleting %s" % filepaths_file)
    os.remove(filepaths_file)

# List all assay folders found under base directory
all_assays = [join(BASE_DIRECTORY, x) for x in os.listdir(BASE_DIRECTORY)]
all_assays = sorted(filter(os.path.isdir, all_assays))
logging.info("Found %g folders under %s" % (len(all_assays), BASE_DIRECTORY))

# Loop over subset of assay folders delimited by START and STOP
assays = all_assays[START - 1:STOP]
nfiles = 0
nfolders = 0
logging.info("Generating %s for %g folders" % (filepaths_file, len(assays)))
for assay in assays:
    logging.debug("Finding cells under %s" % assay)
    # Retrieve individual cell per assays excluding calibration folders
    cells = [x for x in glob(assay + "/*") if not x.endswith("Calibration")]
    for cell in cells:
        for t in IMAGE_TYPES:
            folder = cell + "/%s/*" % IMAGE_TYPES[t]
            tifs = sorted([x for x in glob(folder)
                          if not x.endswith("Thumbs.db")])
            logging.debug("Found %g original files under %s" % (
                         len(tifs), folder))
            nfolders = nfolders + 1
            with open(filepaths_file, 'a') as f:
                for tif in tifs:
                    f.write("Dataset:name:%s\t%s\t%s\n" % (
                            basename(assay) + "_%s" % t,
                            tif,
                            basename(cell) + basename(tif)[-10:-4]))
                    nfiles = nfiles + 1

logging.info("Listed %g files to import, located in %g folders" %
             (nfiles, nfolders))
