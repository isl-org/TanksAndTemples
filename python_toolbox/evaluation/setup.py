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
# This python script is for downloading dataset from www.tanksandtemples.org
# The dataset has a different license, please refer to
# https://tanksandtemples.org/license/


# ----------------------------------------------------------------------------
# INSTRUCTION
# ----------------------------------------------------------------------------

# STEP 0) Specify the path where training dataset folder is located.
# Define DATASET_DIR like below:
# DATASET_DIR = "C:/data/TanksAndTemples/evaluation/" # windows
# DATASET_DIR = "/Users/[user_id]/data/TanksAndTemples/evaluation/" # Mac
# DATASET_DIR = "/home/[user_id]/data/TanksAndTemples/evaluation/" # Ubuntu
# Each dataset folder should have specific folder structure.
# As an example, for "Ignatius" dataset,
# Ignatius/
#  - Ignatius.ply				# Ground truth geometry acquired by high-fidelity 3D Scanner
#  - Ignatius.json 				# Area cropping information to limit spatial boundary for evaluation
#  - Ignatius_COLMAP_SfM.log	# Reference camera pose obtained by successful reconstruction algorithm
#  - Ignatius_trans.txt			# Transformation matrix that aligns reference pose with ground truth
# TanksAndTemples trainning dataset with this folder structure can be download from
# https://drive.google.com/open?id=1VDHEqGAuLyGa7Bv3lGOr1KX2RhPbHLxw
DATASET_DIR = None

# STEP 1) this evaluation script require Open3D python binding
# to install Open3D, please start from http://open3d.org/docs/getting_started.html

# STEP 2) specify path to where Open3D build is
# Define OPEN3D_BUILD_PATH like below:
# OPEN3D_BUILD_PATH = "C:/Open3D/build/" # Windows
# OPEN3D_BUILD_PATH = "/Users/[user_id]/Open3D/build/" # Mac
# OPEN3D_BUILD_PATH = "/home/[user_id]/Open3D/build/" # Ubuntu
OPEN3D_BUILD_PATH = None

# STEP 3) specify path to where
# py3d.so, py3d_[python_version].so or py3d.lib is located
# For example, use one of these:
# OPEN3D_PYTHON_LIBRARY_PATH = OPEN3D_BUILD_PATH + "lib/Release/" # Windows
# OPEN3D_PYTHON_LIBRARY_PATH = OPEN3D_BUILD_PATH + "lib/" # Mac/Ubuntu
OPEN3D_PYTHON_LIBRARY_PATH = OPEN3D_BUILD_PATH + None

# STEP 4) specify path to where
# Open3D"s experimental applications (ViewDistances and ConvertPointCloud)
# For example, use one of these
# OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + "bin/Experimental/Release/" # Windows
# OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + "bin/Experimental/" # Mac/Ubuntu
OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + None

# STEP 5) Set the names for your reconstruction log and reconstruction files
# For example, define MY_LOG_POSTFIX and MY_RECONSTRUCTION_POSTFIX like below:
# MY_LOG_POSTFIX = "_your_camera_poses.log"
# MY_RECONSTRUCTION_POSTFIX = "_your_reconstruction.ply"
# and place _your_camera_poses.log and _your_reconstruction.ply in DATASET_DIR/Ignatius.
# Do the same thing for other scenes.
MY_LOG_POSTFIX = None
MY_RECONSTRUCTION_POSTFIX = None

# ----------------------------------------------------------------------------
# END OF INSTRUCTION
# ----------------------------------------------------------------------------

# some global parameters - do not modify
scenes_tau_dict = {
	"Barn": 0.01,
	"Caterpillar": 0.005,
	"Church": 0.025,
	"Courthouse": 0.025,
	"Ignatius": 0.003,
	"Meetingroom": 0.01,
	"Truck": 0.005}

if OPEN3D_BUILD_PATH is None:
	raise SystemExit("Error:: [OPEN3D_BUILD_PATH] in setup.py is not defined")
if OPEN3D_PYTHON_LIBRARY_PATH is None:
	raise SystemExit("Error:: [OPEN3D_PYTHON_LIBRARY_PATH] in setup.py is not defined")
if OPEN3D_EXPERIMENTAL_BIN_PATH is None:
	raise SystemExit("Error:: [OPEN3D_EXPERIMENTAL_BIN_PATH] in setup.py is not defined")
if MY_LOG_POSTFIX is None:
	raise SystemExit("Error:: [MY_LOG_POSTFIX] in setup.py is not defined")
if MY_RECONSTRUCTION_POSTFIX is None:
	raise SystemExit("Error:: [MY_RECONSTRUCTION_POSTFIX] in setup.py is not defined")

import sys
sys.path.append(OPEN3D_PYTHON_LIBRARY_PATH)
try:
    from py3d import *
except:
    raise SystemExit("Error:: please correctly set paths for Open3D in setup.py")
