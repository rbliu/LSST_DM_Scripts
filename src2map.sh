#!/bin/bash
#Author:R.B.Liu
########################################################################
# Notes:
# This script is used to generate fiatmap from a given src fits table.
# 1. Make sure you have print_fiat_header.py and readout_src_2.0.py under the same directory with this script.
# 2. It also needs numpy, astropy and pyfits -- they are included in DMstack.
# 3. Make sure fiat tools (eg. fiatfilter, fiatmap) are already installed.
#    (In our lab, you need to add "export PATH=$PATH:/usr/dist/dls/bin" to your ~/.bashrc file.)
# 4. Modify wdir and src_fits by yourself, as well as the parameters in fiatfilter& fiatmap.
# 5. (Updated 2019/7/1) obs_file is working with DM v13.0 (Python 2). If you are using a later version of DM ot Python, please ignore this script!
########################################################################

# Set the filenames. Modify wdir and src_fits by yourself!
wdir="/Users/rliu/Downloads/test/"  #working directory where the files are. DON'T miss the '/' in the path!
src_fits="SRC-806305-10.fits"      #output src fits file from DMstack
########################################################################

echo "You are processing the src catalog: "
echo ${wdir}${src_fits}
echo " "

filename=${src_fits%.*}            #extract the filename without extension
src_cat=${filename}.fcat           #fiat catalog file to save the data
filtered_cat=${filename}f.fcat     #filtered catalog after fiatfilter

r_inner=300                        #inner radius for fiatmap
r_outer=20000                      #outer radius for fiatmap
fmap=${filename}fmap.fits          #the output fiatmap file

echo "Converting the src fits file to fiat catalog..."
# Generate the ASCII catalog with fiat headers
python print_fiat_header.py ${wdir}${src_fits} > ${wdir}${src_cat}
python readout_src_2.0.py ${wdir}${src_fits} >> ${wdir}${src_cat}

echo "Filtering the fiat catalog..."
# Filter the catalog. These parameters are tested with CFHT data. MODIFY them according to your image!
fiatfilter "base_GaussianFlux_flux > 500 &&\
base_GaussianFlux_flux < 4000000 &&\
calib_psfUsed < 0.5 &&\
base_ClassificationExtendedness_value > 0.5 &&\
base_PixelFlags_flag_interpolatedCenter < 0.5 &&\
(ext_shapeHSM_HsmShapeRegauss_e1)**2 + (ext_shapeHSM_HsmShapeRegauss_e2)**2 < 1.5 &&\
base_SdssShape_xx + base_SdssShape_yy < 200 &&\
base_SdssShape_xx > 1 &&\
base_SdssShape_yy > 1" ${wdir}${src_cat} > ${wdir}${filtered_cat}

# Modify the fiat header to match fiatmap requirement
sed -i -e 's/ext_shapeHSM_HsmSourceMoments_xx/ixx/g' ${wdir}${filtered_cat}
sed -i -e 's/ext_shapeHSM_HsmSourceMoments_yy/iyy/g' ${wdir}${filtered_cat}
sed -i -e 's/ext_shapeHSM_HsmSourceMoments_xy/ixy/g' ${wdir}${filtered_cat}
sed -i -e 's/ext_shapeHSM_HsmSourceMoments_x/x/g' ${wdir}${filtered_cat}
sed -i -e 's/ext_shapeHSM_HsmSourceMoments_y/y/g' ${wdir}${filtered_cat}
# If you are using macOS, use the following 5 lines instead of the above lines
# sed "-i" "" "-e" 's/ext_shapeHSM_HsmSourceMoments_xx/ixx/g' ${wdir}${filtered_cat}
# sed "-i" "" "-e" 's/ext_shapeHSM_HsmSourceMoments_yy/iyy/g' ${wdir}${filtered_cat}
# sed "-i" "" "-e" 's/ext_shapeHSM_HsmSourceMoments_xy/ixy/g' ${wdir}${filtered_cat}
# sed "-i" "" "-e" 's/ext_shapeHSM_HsmSourceMoments_x/x/g' ${wdir}${filtered_cat}
# sed "-i" "" "-e" 's/ext_shapeHSM_HsmSourceMoments_y/y/g' ${wdir}${filtered_cat}

echo "Generating fiat map..."
# Generate the kappa map
fiatmap ${wdir}${filtered_cat} ${r_inner} ${r_outer} ${wdir}${fmap}

echo "Done! fiatmap saved at"
echo ${wdir}${fmap}
