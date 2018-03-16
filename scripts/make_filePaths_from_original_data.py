#!/usr/bin/env python
# Generate filePaths tsv file with raw files

from glob import glob
import os
from os.path import basename, join
import sys

BASE_DIRECTORY = "/uod/idr/filesets/idr0041-cai-mitoticatlas/"
LIMIT = 2

if not os.path.exists(BASE_DIRECTORY):
    print "Cannot find the raw data directory. Exiting."
    sys.exit(0)

# Determine base location for pattern files
metadata_dir = os.path.dirname(os.path.realpath(__file__))
filepaths_file = join(metadata_dir, "..", "experimentA",
                      "idr0041-experimentA-filePaths.tsv")

if os.path.exists(filepaths_file):
    os.remove(filepaths_file)
print "Creating %s" % filepaths_file

# List all assay folders under base directory
assays = [join(BASE_DIRECTORY, x) for x in os.listdir(BASE_DIRECTORY)]
assays = sorted(filter(os.path.isdir, assays))
for assay in assays[:LIMIT]:
    # Retrieve individual cell per assays excluding calibration folders
    cells = [x for x in glob(assay + "/*") if not x.endswith("Calibration")]
    for cell in cells:
        # List raw and concatenated TIFF files
        rawtifs = sorted([x for x in glob(cell + "/rawtif/*")
                          if not x.endswith("Thumbs.db")])
        masktifs = sorted([x for x in glob(cell + "/masktif/*")
                          if not x.endswith("Thumbs.db")])
        conctifs = sorted([x for x in glob(cell + "/conctif/*")
                           if not x.endswith("Thumbs.db")])

        with open(filepaths_file, 'a') as f:
            for rawtif in rawtifs:
                f.write("Dataset:name:%s\t%s\t%s\n" % (
                    basename(assay) + "_raw", rawtif,
                    basename(rawtif)[:-4]))

            for masktif in masktifs:
                f.write("Dataset:name:%s\t%s\t%s\n" % (
                    basename(assay) + "_mask", masktif,
                    basename(masktif)[:-4]))

            for conctif in conctifs:
                f.write("Dataset:name:%s\t%s\t%s\n" % (
                    basename(assay) + "_conc", conctif,
                    basename(conctif)[:-4]))
