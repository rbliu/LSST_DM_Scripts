#!/bin/bash
#Author:R.B.Liu
########################################################################
# Notes:
# This script is used to generate ds9 region file of PSF stars from a given src fits table.
# 1. Make sure you have print_fiat_header.py and readout_src_2.0.py under the same directory with this script.
# 2. It also needs numpy, astropy and pyfits -- they are included in DMstack.
# 3. Make sure fiat tools (eg. fiatfilter, fiatmap) are already installed.
#    (In our lab, you need to add "export PATH=$PATH:/usr/dist/dls/bin" to your ~/.bashrc file.)
# 4. Modify wdir and src_fits by yourself, as well as the parameters in fiatfilter.
########################################################################

# Set the filenames. Modify wdir and src_fits by yourself!
wdir="/Users/rliu/github/Useful_Scripts/DM_stack/"  #working directory where the files are
src_fits="cluster40_src.fits"      #output src fits file from DMstack
########################################################################

echo "You are processing the src catalog: "
echo ${wdir}${src_fits}
echo " "

filename=${src_fits%.*}            #extract the filename without extension
src_cat=${filename}.fcat           #fiat catalog file to save the data
filtered_cat=${filename}_psf.fcat     #filtered catalog after fiatfilter
reg_file=${filename}_psf.reg

echo "Converting the src fits file to fiat catalog..."
# Generate the ASCII catalog with fiat headers
python print_fiat_header.py ${wdir}${src_fits} > ${wdir}${src_cat}
python readout_src_2.0.py ${wdir}${src_fits} >> ${wdir}${src_cat}

echo "Filtering the fiat catalog..."
# Filter the catalog to keep only the PSFused objects!
fiatfilter "calib_psfUsed > 0.5" ${wdir}${src_cat} > ${wdir}${filtered_cat}

# Select only the x y columns: Make sure the column numbers are correct!
fiatrecolumn 132,133 ${wdir}${filtered_cat} > ${wdir}${reg_file}

echo "Done! PSF region file saved at"
echo ${wdir}${reg_file}
