#!/usr/bin/env python
# Generate filePaths tsv file with raw files

from glob import glob
import logging
import os
from os.path import basename, join
import sys

BASE_DIRECTORY = "/uod/idr/filesets/idr0041-cai-mitoticatlas/"
LIMIT = 2

IMAGE_TYPES = {
    'raw': 'rawtif',
    'mask': 'masktif',
    'conc': 'conctif',
}

logging.basicConfig(level=logging.INFO)
if not os.path.exists(BASE_DIRECTORY):
    print "Cannot find the raw data directory. Exiting."
    sys.exit(0)

# Determine base location for pattern files
metadata_dir = os.path.dirname(os.path.realpath(__file__))
filepaths_file = join(metadata_dir, "..", "experimentA",
                      "idr0041-experimentA-filePaths.tsv")

if os.path.exists(filepaths_file):
    os.remove(filepaths_file)
logging.info("Deleting %s" % filepaths_file)

# List all assay folders under base directory
assays = [join(BASE_DIRECTORY, x) for x in os.listdir(BASE_DIRECTORY)]
assays = sorted(filter(os.path.isdir, assays))
for assay in assays[:LIMIT]:
    logging.info("Finding cells under %s" % assay)
    # Retrieve individual cell per assays excluding calibration folders
    cells = [x for x in glob(assay + "/*") if not x.endswith("Calibration")]
    for cell in cells:
        for t in IMAGE_TYPES:
            folder = cell + "/%s/*" % IMAGE_TYPES[t]
            tifs = sorted([x for x in glob(folder)
                          if not x.endswith("Thumbs.db")])
            logging.info("Found %g original files under %s" % (
                         len(tifs), folder))

            with open(filepaths_file, 'a') as f:
                for tif in tifs:
                    f.write("Dataset:name:%s\t%s\t%s\n" % (
                            basename(assay) + "_%s" % t,
                            tif,
                            basename(cell) + basename(tif)[-10:-4]))
