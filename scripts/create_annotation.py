#!/usr/bin/env python
# Generate annotation.csv from original assays file

import logging
import os
import os.path
import warnings
import pandas
warnings.simplefilter(action='ignore', category=FutureWarning)


IMAGEFILEPATH = 'Comment [Image File Path]'
ASSAYS_PATTERN = '^mitotic_cell_atlas/([\w-]+)/.*$'
CELL_PATTERN = '^mitotic_cell_atlas/[\w-]+/(\w+)/.*$'
TYPE_PATTERN = '^.*/(\w+)tif$'
DEBUG = int(os.environ.get("DEBUG", logging.INFO))

logging.basicConfig(level=DEBUG)

# Read the assays file
scripts_dir = os.path.dirname(os.path.realpath(__file__))
assays_file = os.path.join(
    scripts_dir, "..", "experimentA", "idr0041-assays.txt")
logging.info("Reading %s" % assays_file)
df = pandas.read_csv(assays_file, sep='\t')
#df = df[df[IMAGEFILEPATH].str.contains('170428_MAD2L1gfpcM11')]

# Generate the dataset and image name columns
logging.debug("Generating dataset and image name columns")
df['Dataset Name'] = df['Assay Name'] + \
    '_' + df[IMAGEFILEPATH].str.extract(TYPE_PATTERN)
df['Image Name'] = df[IMAGEFILEPATH].str.extract(CELL_PATTERN) + \
    df['Image File'].str[-10:-4]
df['Characteristics [Cell ID]'] = df[IMAGEFILEPATH].str.extract(CELL_PATTERN)

# Reorder columns to start with Dataset and Image names
logging.debug("Generating dataset and image name columns")
cols = df.columns.tolist()
cols.pop(cols.index('Assay Name'))
cols.pop(cols.index('Image File'))
cols.pop(cols.index('Comment [Image File Path]'))
cols.insert(0, cols.pop(cols.index('Image Name')))
cols.insert(0, cols.pop(cols.index('Dataset Name')))
df = df[cols]

# Create annotation
csv_file = os.path.join(
    scripts_dir, "..", "experimentA", "idr0041-experimentA-annotation.csv")
logging.info("Generating %s" % csv_file)
df.to_csv(csv_file, sep=',', index=False)
