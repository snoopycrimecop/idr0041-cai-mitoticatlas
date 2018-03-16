#!/usr/bin/env python
# Generate annotation.csv from original assays file

import pandas

IMAGEFILEPATH = 'Comment [Image File Path]'
CELL_PATTERN = '^mitotic_cell_atlas/(\w+)/.*$'
TYPE_PATTERN = '^.*/(\w+)tif$'

# Read the assays file
df = pandas.read_csv('experimentA/idr0041-assays.txt', sep='\t')
kif11 = df[df[IMAGEFILEPATH].str.contains('KIF11')]

# Generate the dataset and image name columns
kif11['Dataset Name'] = kif11[IMAGEFILEPATH].str.extract(CELL_PATTERN) + \
    '_' + kif11[IMAGEFILEPATH].str.extract(TYPE_PATTERN)
kif11['Image Name'] = kif11['Image File'].str[:-4]

# Reorder columns
cols = kif11.columns.tolist()
cols = cols[-1:] + cols[:-1]
cols.insert(0, cols.pop(cols.index('Dataset Name')))
kif11 = kif11[cols]

# Create annotation
kif11.to_csv('experimentA/idr0041-experimentA-annotation.csv', sep=',',
             index=False)
