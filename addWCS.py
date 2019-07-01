#from __future__ import division, print_function
import numpy as np
from astropy import wcs
from astropy.io import fits

w = wcs.WCS(naxis=2)
# what is the center pixel of the X-Y grid
w.wcs.crpix = [1800.0, 1800.0]
# what is the coordinate of that pixel
w.wcs.crval = [0.1, 0.1]
# what is the pixel scale (deg/pix) in longitude and latitude -- 0.2arcsec/pix
w.wcs.cdelt = np.array([-5.55555555555556E-05,5.55555555555556E-05])
# it is a tangential projection
w.wcs.ctype = ["RA---TAN", "DEC--TAN"]

wcsheader = w.to_header()
print wcsheader

# write wcs to header
d = fits.open('trial00.fits', mode='update')
h = d[0].header
h += wcsheader

# h['CTYPE1'] = 'RA---TAN'
# h['CTYPE2'] = 'DEC--TAN'
# h['CRPIX1'] = 1800.
# h['CRVAL1'] = 0.1
# h['CRPIX2'] = 1800.
# h['CRVAL2'] = 0.1
# h['CD1_1']  = 5.55555555555556E-05
# h['CD1_2']  =                  -0.
# h['CD2_1']  =                   0.
# h['CD2_2']  = 5.55555555555556E-05
# h['EQUINOX'] = 2000.
# h['EPOCH']  =  2000.
# h['RADESYS'] = 'J2000'

d.flush()
d.close()
print("Fake WCS infomation added!")
