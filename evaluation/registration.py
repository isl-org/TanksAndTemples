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

from setup import *
import copy
import numpy as np

MAX_POINT_NUMBER = 1e6

def registration_unif(source, gt_target, init_trans,
		crop_volume, threshold, max_itr, max_size = 4*MAX_POINT_NUMBER,
		verbose = True):
	if verbose:
		print("[Registration] threshold: %f" % threshold)
		set_verbosity_level(VerbosityLevel.Debug)
	s = copy.deepcopy(source)
	s.transform(init_trans)
	s = crop_volume.crop_point_cloud(s)
	s_len = len(s.points)
	if(s_len>max_size):
		ds_rate = int(round(s_len/float(max_size)))
		s = uniform_down_sample(s, ds_rate)

	t = copy.deepcopy(gt_target)
	t = crop_volume.crop_point_cloud(t)
	t_len = len(t.points)
	if t_len>max_size:
		ds_rate = int(round(t_len/float(max_size)))
		t = uniform_down_sample(t, ds_rate)

	reg = registration_icp(s, t, threshold, np.identity(4),
			TransformationEstimationPointToPoint(True),
			ICPConvergenceCriteria(1e-6, max_itr))
	reg.transformation = np.matmul(reg.transformation, init_trans)
	return reg

def registration_vol_ds(source, gt_target, init_trans,
		crop_volume, voxel_size, threshold, max_itr,
		verbose = True):
	if verbose:
		print("[Registration] voxel_size: %f, threshold: %f"
				% (voxel_size, threshold))
		set_verbosity_level(VerbosityLevel.Debug)
	s = copy.deepcopy(source)
	s.transform(init_trans)
	s = crop_volume.crop_point_cloud(s)
	s = voxel_down_sample(s, voxel_size)

	t = copy.deepcopy(gt_target)
	t = crop_volume.crop_point_cloud(t)
	t = voxel_down_sample(t, voxel_size)

	reg = registration_icp(s, t, threshold, np.identity(4),
			TransformationEstimationPointToPoint(True),
			ICPConvergenceCriteria(1e-6, max_itr))
	reg.transformation = np.matmul(reg.transformation, init_trans)
	return reg
