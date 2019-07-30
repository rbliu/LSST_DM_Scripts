# -*- coding: utf-8 -*-
#!/usr/bin/env python
## last modified by Robert Liu at 7/29/2019
## This script is used to extract Date and Time from 'date' keyword of the input FITS header and write it to a new 'DTUTC' keyword, which is required by DMstack v17.0.1 (astrom_metadata_translator) but lacked in DECam pipeline after 2017/11.

import re
import sys
import numpy as np
from astropy.io import fits
from astropy.io.fits import getdata

if len(sys.argv) != 2:
    print("Usage: python fitsAddDT.py {fits_image}", file=sys.stderr)
    exit(1);
fits1 = sys.argv[1]


hdu = fits.open(fits1, mode='update')
date_string = hdu[0].header['date']
print('Date and time when this FITS was generated: ', date_string)

hdu[0].header.append(('DTUTC', date_string, 'Date Time'), end=True)
hdu.close()

print('DTUTC keyword added to the FITS file!\n')
