#!/bin/bash

# ----------------------------------------------------------------------------
# -                   TanksAndTemples Website Toolbox                        -
# -                    http://www.tanksandtemples.org                        -
# ----------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2017
# Arno Knapitsch <arno.knapitsch@gmail.com >
# Jaesik Park <syncle@gmail.com>
# Qian-Yi Zhou <Qianyi.Zhou@gmail.com>
# Vladlen Koltun <vkoltun@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ----------------------------------------------------------------------------
#
# This script generates a COLMAP reconstruction from a numbe rof input imagess
# Usage: sh get_colmap_reconstruction.sh input_folder/ output_folder/

iname=$1
outf=$2

DATABASE=sample_reconstruction.db

PROJECT_PATH=${outf}
mkdir -p ${PROJECT_PATH}

cp -n ${iname}*.jpg ${PROJECT_PATH}

~/software/colmap/build/src/exe/feature_extractor \
    --database_path ${DATABASE} \
    --image_path ${PROJECT_PATH} \
	--ImageReader.camera_model RADIAL \
	--ImageReader.single_camera 1 \
	--use_gpu 0
	


~/software/colmap/build/src/exe/exhaustive_matcher \
    --database_path ${DATABASE} \
    --SiftMatching.use_gpu 1 
    
mkdir ${PROJECT_PATH}/sparse

~/software/colmap/build/src/exe/mapper \
    --database_path ${DATABASE} \
    --image_path ${PROJECT_PATH} \
    --export_path ${PROJECT_PATH}/sparse

mkdir ${PROJECT_PATH}/dense

~/software/colmap/build/src/exe/image_undistorter \
    --image_path ${PROJECT_PATH} \
    --input_path ${PROJECT_PATH}/sparse/0/ \
    --output_path ${PROJECT_PATH}/dense \
    --output_type COLMAP --max_image_size 1500


~/software/colmap/build/src/exe/dense_stereo \
    --workspace_path $PROJECT_PATH/dense \
    --workspace_format COLMAP \
    --DenseStereo.geom_consistency true

~/software/colmap/build/src/exe/dense_fuser \
    --workspace_path $PROJECT_PATH/dense \
    --workspace_format COLMAP \
    --input_type geometric \
    --output_path $PROJECT_PATH/dense/fused.ply


