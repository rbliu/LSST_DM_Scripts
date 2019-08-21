# -*- coding: utf-8 -*-
#!/usr/bin/env python
## last modified by Robert Liu at 7/29/2019
## This script is used to extract data (and WCS info) in the image extension of a coadd patch.
## Ext 0 = primaryHDU, Ext 1 = image, Ext 2 = mask, Ext 3 = variancce.
## Then, the output fits file can be used by SWarp to assemble a mosaic coadd image.

import re
import sys
import numpy as np
from astropy.io import fits
from astropy import wcs

if len(sys.argv) != 3:
    print("Usage: python coaddExtract.py {coadd_image} {extracted_image}", file=sys.stderr)
    exit(1);
coadd_patch = sys.argv[1]
extracted_patch = sys.argv[2]

# Open the fits image
hdu = fits.open(coadd_patch)

# Create a new HDU. Save the data of Ext1 to it.
hdu1 = fits.PrimaryHDU(hdu[1].data)
print('Coadd patch loaded.')

# Extract WCS info and append to the new HDU.
w = wcs.WCS(hdu[1].header)
wcs_keys = w.to_header()
hdu1.header += wcs_keys
print('WCS information appened.')

# Write the new HDU
hdu1.writeto(extracted_patch)
print('New coadd image saved!\n')
