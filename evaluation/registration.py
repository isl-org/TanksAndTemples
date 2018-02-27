from setup_open3d import *
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
