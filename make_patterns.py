#!/usr/bin/env python

from glob import glob
import os
from os.path import basename, join
from pyidr.file_pattern import FilePattern

TIMEPOINTS = 40

base = "/uod/idr/filesets/idr0041-cai-mitoticatlas/"
patterns_base = join(os.path.dirname(os.path.realpath(__file__)), "patterns")
print "Creating patterns from %s, saving under %s" % (base, patterns)

assays = [join(base, x) for x in os.listdir(base)]
assays = filter(os.path.isdir, assays)
for assay in assays:
    cells = [x for x in glob(assay + "/*") if not x.endswith("Calibration")]
    for cell in cells:
        rawtifs = sorted([x for x in glob(cell + "/rawtif/*")
            if not x.endswith("Thumbs.db")])
        raw_pattern = join(cell, "rawtif",
            basename(rawtifs[0])[:-6] + "<01-%g>" % TIMEPOINTS + ".tif")
        assert list(FilePattern(raw_pattern).filenames()) == rawtifs

        pattern_dir = join(patterns_base, basename(assay), basename(cell))
        if not os.path.exists(pattern_dir):
            os.makedirs(pattern_dir)
        pattern_file =  join(pattern_dir, "rawtif.pattern")
        with open(pattern_file, 'w') as f:
            print "Writing %s" % pattern_file
            # f.write(raw_pattern)
