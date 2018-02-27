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

# STEP 0) Specify the path where dataset folder is located.
# for example,
# BASE_DIR = "C:/TanksAndTemples/evaluation/data/"
BASE_DIR = "C:/git/TanksAndTemples/evaluation/data/"

# STEP 1) this evaluation script require Open3D python binding
# to install Open3D, please start from http://open3d.org/docs/getting_started.html

# STEP 2) specify path to where Open3D build is
# for example, modify and use one of these
# OPEN3D_BUILD_PATH = 'C:/Open3D/build/' # Windows
# OPEN3D_BUILD_PATH = '/Users/[user_id]/Open3D/build/' # Mac
# OPEN3D_BUILD_PATH = '/home/[user_id]/Open3D/build/' # Ubuntu
OPEN3D_BUILD_PATH = 'C:/git/Open3D/build/'

# STEP 3) specify path to where
# py3d.so, py3d_[python_version].so or py3d.lib is located
# for example, use one of these
OPEN3D_PYTHON_LIBRARY_PATH = OPEN3D_BUILD_PATH + 'lib/Release/' # Windows
# OPEN3D_PYTHON_LIBRARY_PATH = OPEN3D_BUILD_PATH + 'lib/' # Mac
# OPEN3D_PYTHON_LIBRARY_PATH = OPEN3D_BUILD_PATH + 'lib/' # Ubuntu

# STEP 4) specify path to where
# Open3D's experimental applications (ViewDistances and ConvertPointCloud)
# for example, use one of these
OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + 'bin/Experimental/Release/' # Windows
# OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + 'bin/Experimental/' # Mac
# OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + 'bin/Experimental/' # Ubuntu

# STEP 5) specify path to where
# Open3D's experimental applications (ViewDistances and ConvertPointCloud)
# for example, use one of these
OPEN3D_BIN_PATH = OPEN3D_BUILD_PATH + 'bin/Release/' # Windows
# OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + 'bin/' # Mac
# OPEN3D_EXPERIMENTAL_BIN_PATH = OPEN3D_BUILD_PATH + 'bin/' # Ubuntu

# some global parameters - do not modify
dTau_dict = {
	"Barn":0.01,
	"Caterpillar":0.005,
	"Church":0.025,
	"Courthouse":0.025,
	"Ignatius":0.003,
	"Meetingroom":0.01,
	"Truck":0.005}

scenes = [
	"Barn",
	"Caterpillar",
	"Church",
	"Courthouse",
	"Ignatius",
	"Meetingroom",
	"Truck"]

if OPEN3D_BUILD_PATH is None:
	raise SystemExit('Error:: please set [OPEN3D_BUILD_PATH] in setup.py')
if OPEN3D_PYTHON_LIBRARY_PATH is None:
	raise SystemExit('Error:: please set [OPEN3D_PYTHON_LIBRARY_PATH] in setup.py')
if OPEN3D_EXPERIMENTAL_BIN_PATH is None:
	raise SystemExit('Error:: please set [OPEN3D_EXPERIMENTAL_BIN_PATH] in setup.py')

import sys
sys.path.append(OPEN3D_PYTHON_LIBRARY_PATH)
from py3d import *
