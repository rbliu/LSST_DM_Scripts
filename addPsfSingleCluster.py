import re, os, sys
import numpy as np
import pyfits
from astropy.io import fits
import random


if len(sys.argv) != 2:
    print >>sys.stderr, "Usage: python addPsfSingleCluster.py {/path/to/LSST/simulation} "
    exit(1);
image = sys.argv[1]

#sim = pyfits.open('trial1_LSST_convolved_noise.fits', mode='update')
sim = fits.open('%s' %(image), mode='update')
psf = fits.open('psf_LSST20000.fits')
sim[0].data = sim[0].data/6000.0

for i in range(0,200):
    xput = random.randint(1,3388)
    yput = random.randint(1,3388)
    sim[0].data[yput-1:yput+152, xput-1:xput+152] += psf[0].data
    print i, xput, yput

sim.flush()
sim.close()
psf.close()
