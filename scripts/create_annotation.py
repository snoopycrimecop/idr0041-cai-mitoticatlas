#!/usr/bin/env python
# Generate annotation.csv from original assays file

import pandas

IMAGEFILEPATH = 'Comment [Image File Path]'
CELL_PATTERN = '^mitotic_cell_atlas/(\w+)/.*$'
TYPE_PATTERN = '^.*/(\w+)tif$'

# Read the assays file
df = pandas.read_csv('experimentA/idr0041-assays.txt', sep='\t')

# Generate the dataset and image name columns
df['Dataset Name'] = df[IMAGEFILEPATH].str.extract(CELL_PATTERN) + \
    '_' + df[IMAGEFILEPATH].str.extract(TYPE_PATTERN)
df['Image Name'] = df['Image File'].str[:-4]

# Reorder columns to start with Dataset and Image names
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
cols.insert(0, cols.pop(cols.index('Dataset Name')))
df = df[cols]

# Create annotation
df.to_csv('../experimentA/idr0041-experimentA-annotation.csv', sep=',',
             index=False)
