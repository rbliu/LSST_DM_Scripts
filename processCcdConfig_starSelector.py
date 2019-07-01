
config.charImage.repair.cosmicray.nCrPixelMax=10000000

# Use psfex instead of pca
import lsst.meas.extensions.psfex.psfexPsfDeterminer
config.charImage.measurePsf.psfDeterminer.name='psfex'

config.isr.noise=5.0
config.isr.saturation=50000

config.charImage.measureApCorr.starSelector['objectSize'].fluxMin=25000
config.charImage.measureApCorr.starSelector['objectSize'].fluxMax=300000

config.charImage.measureApCorr.starSelector['secondMoment'].fluxLim=25000
