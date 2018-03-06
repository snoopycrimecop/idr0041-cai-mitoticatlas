#!/usr/bin/env python

from glob import glob
import os
from os.path import basename, join
from pyidr.file_pattern import FilePattern

TIMEPOINTS = 40
BASE_DIRECTORY = "/uod/idr/filesets/idr0041-cai-mitoticatlas/"

# Determine base location for pattern files
patterns_base = join(os.path.dirname(os.path.realpath(__file__)), "patterns")
print "Creating patterns from %s, saving under %s" % (base, patterns_base)

# List all assay folders under base directory
assays = [join(BASE_DIRECTORY, x) for x in os.listdir(base)]
assays = filter(os.path.isdir, assays)
for assay in assays:
    # Retrieve individual cell per assays excluding calibration folders
    cells = [x for x in glob(assay + "/*") if not x.endswith("Calibration")]
    for cell in cells:
        # List raw and concatenated TIFF files
        rawtifs = sorted([x for x in glob(cell + "/rawtif/*")
                          if not x.endswith("Thumbs.db")])
        conctifs = sorted([x for x in glob(cell + "/conctif/*")
                           if not x.endswith("Thumbs.db")])

        # Construct and validate pattern strings
        raw_pattern = join(cell, "rawtif",
            basename(rawtifs[0])[:-6] + "<01-%g>" % TIMEPOINTS + ".tif")
        assert list(FilePattern(raw_pattern).filenames()) == rawtifs
        conc_pattern = join(cell, "conctif",
            basename(rawtifs[0])[:-6] + "<01-%g>" % TIMEPOINTS + ".tif")
        assert list(FilePattern(conc_pattern).filenames()) == conctifs

        # Create pattern files on disk
        pattern_dir = join(patterns_base, basename(assay), basename(cell))
        if not os.path.exists(pattern_dir):
            os.makedirs(pattern_dir)
        raw_pattern_file = join(pattern_dir, "rawtif.pattern")
        conc_pattern_file = join(pattern_dir, "conctif.pattern")
        with open(raw_pattern_file, 'w') as f:
            print "Writing %s" % raw_pattern_file
            f.write(raw_pattern)
        with open(conc_pattern_file, 'w') as f:
            print "Writing %s" % conc_pattern_file
            f.write(conc_pattern)
