# -*- coding: utf-8 -*-
#!/usr/bin/env python
## last modified by Robert Liu at 6/20/2018
## This script is used to extract header and catalog from a (DM stack output) src fits file, and save it as the fiat style.

import re
import sys
import numpy as np
from astropy.io import fits

if len(sys.argv) != 2:
    print("Usage: python src2fcat_py3.py {source_fits_file} > {fiat_file}", file=sys.stderr)
    exit(1);
srcfits = sys.argv[1]

# Load sources and print the fiat header
if srcfits=='':
	srcfits = 'src.fits'

data_table, header_table = fits.getdata('%s' %(srcfits), 1, header=True)

print('# fiat 1.0')

# Print all the flag names
# for i in range(len(header_table['TFLAG*'])):
#     print('# TTYPE' + str(i+1) + ' = ' + header_table['TFLAG*'][i])

# Print all the column names except the 1st column "flags"
# for i in range(len(header_table['TTYPE*'])-1):
#     print('# TTYPE' + str(len(header_table['TFLAG*'])+i+1) + ' = ' + header_table['TTYPE*'][i+1])
for i in range(len(header_table['TTYPE*'])-1):
    print('# TTYPE' + str(i+1) + ' = ' + header_table['TTYPE*'][i+1])


# Print the catalog part
d = fits.open('%s' %(srcfits))
data = d[1].data
cols = d[1].columns
header_table = d[1].header

newcols = cols.names

vecs = data.field('id')[np.newaxis].T

# newcols.remove('flags')
# newcols.remove('id')
for i in newcols[2:]:
    v=data.field(i)[np.newaxis].T
    # vecs = np.hstack((vecs,v[:,None]))
    vecs = np.hstack((vecs, v))

print('\n'.join(' '.join(str(x) for x in row) for row in vecs))
