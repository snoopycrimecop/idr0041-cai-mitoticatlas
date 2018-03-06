#!/usr/bin/env python

from glob import glob
import os
from os.path import basename, join
from pyidr.file_pattern import FilePattern
import shutil
import sys

TIMEPOINTS = 40
BASE_DIRECTORY = "/uod/idr/filesets/idr0041-cai-mitoticatlas/"
LIMIT = 2

if not os.path.exists(BASE_DIRECTORY):
    print "Cannot find the raw data directory. Exiting."
    sys.exit(0)

# Determine base location for pattern files
metadata_dir = os.path.dirname(os.path.realpath(__file__))
patterns_base = join(metadata_dir, "patterns")
filepaths_file = join(metadata_dir, "experimentA",
                      "idr0041-experimentA-filePaths.tsv")
print "Creating patterns from %s, saving under %s" % (
    BASE_DIRECTORY, patterns_base)

if os.path.exists(patterns_base):
    shutil.rmtree(patterns_base)
if os.path.exists(filepaths_file):
    os.remove(filepaths_file)

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
        conctifs = sorted([x for x in glob(cell + "/conctif/*")
                           if not x.endswith("Thumbs.db")])

        # Construct and validate pattern strings
        raw_pattern = join(
            cell, "rawtif",
            basename(rawtifs[0])[:-6] + "<01-%g>" % TIMEPOINTS + ".tif")
        assert list(FilePattern(raw_pattern).filenames()) == rawtifs
        conc_pattern = join(
            cell, "conctif",
            basename(rawtifs[0])[:-6] + "<01-%g>" % TIMEPOINTS + ".tif")
        assert list(FilePattern(conc_pattern).filenames()) == conctifs

        # Create pattern files on disk
        pattern_dir = join(patterns_base, basename(assay), basename(cell))
        os.makedirs(pattern_dir)
        raw_pattern_file = join(pattern_dir, "rawtif.pattern\n")
        conc_pattern_file = join(pattern_dir, "conctif.pattern\n")
        with open(raw_pattern_file, 'w') as f:
            print "Writing %s" % raw_pattern_file
            f.write(raw_pattern)

        with open(conc_pattern_file, 'w') as f:
            print "Writing %s" % conc_pattern_file
            f.write(conc_pattern)

        with open(filepaths_file, 'w') as f:
            f.write("Dataset:name:%s\t../patterns/%s/%s/%s\n" % (
                basename(assay), basename(assay), basename(cell),
                "rawtif.pattern"))
            f.write("Dataset:name:%s\t../patterns/%s/%s/%s\n" % (
                basename(assay), basename(assay), basename(cell),
                "conctif.pattern"))
