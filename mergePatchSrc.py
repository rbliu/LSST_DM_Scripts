# -*- coding: utf-8 -*-
#!/usr/bin/env python
## last modified by Robert Liu at 6/27/2019
## This script is used to merge DMstack output src files from two neighboring patches. And remove overlapped objects.
## Two neighbor patches have an overlap, where a same object has DIFFERENT ID in two patches. So, we need to match objects by ra & dec.

import re
import sys
import numpy as np
from astropy.io import fits
from astropy.io.fits import getdata

if len(sys.argv) != 4:
    #print >>sys.stderr, "Usage: python mergePatchSrc.py {src_file1} {src_file2} {merged_file}"
    print("Usage: python mergePatchSrc.py {src_file1} {src_file2} {merged_file}", file=sys.stderr)
    exit(1);
srcfits1 = sys.argv[1]
srcfits2 = sys.argv[2]
mergedSrc = sys.argv[3]

# Load sources and print the fiat header
# if srcfits=='':
# 	srcfits = 'src.fits'

# Append one FITS table to the other one
with fits.open(srcfits1) as hdul1:
    with fits.open(srcfits2) as hdul2:
        nrows1 = hdul1[1].data.shape[0]
        nrows2 = hdul2[1].data.shape[0]
        nrows = nrows1 + nrows2
        hdu = fits.BinTableHDU.from_columns(hdul1[1].columns, nrows=nrows)
        for colname in hdul1[1].columns.names:
            hdu.data[colname][nrows1:] = hdul2[1].data[colname]

# The total object number in the merged table
data_sum = hdu.data
print('Sum of objects in two input FITS tables =', data_sum.shape[0])

# Parent and Child objects may have same ra&dec. Filter and keep only Children objects.
data_sum_child = data_sum[data_sum['deblend_nChild']==0]
print('Child object number in the sum FITS tables =', data_sum_child.shape[0])

# Select the ra & dec columns and stack them together
data_slice = np.stack((data_sum_child['coord_ra'], data_sum_child['coord_dec']), axis = 1)

# Get the unique indices of objects with same ra + dec
_, unq_row_indices = np.unique(data_slice, return_index=True, axis=0)

# Select only the unique objects
data_sum_child_unique = data_sum_child[unq_row_indices]
print('Total object number after removing duplicate ones =', data_sum_child_unique.shape[0])

# Update and save the new merged FITS table
hdu.data = data_sum_child_unique
hdu.writeto(mergedSrc)
print('The merged FITS file is saved!\n')
