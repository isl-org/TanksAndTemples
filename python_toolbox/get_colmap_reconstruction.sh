#!/bin/bash

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


