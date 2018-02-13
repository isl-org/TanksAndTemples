from setup_open3d import *
import copy
import numpy as np


def registration_unif(source, gt_target, init_trans, crop_volume, threshold, max_itr, max_size):
    set_verbosity_level(VerbosityLevel.Debug)
    s = copy.deepcopy(source)
    s.transform(init_trans)
    s = crop_volume.crop_point_cloud(s)
    #s = VoxelDownSample(s, voxel_size)
    s_len = len(s.points)
    if(s_len>max_size):
        ds_rate = int(round(s_len/float(max_size)))
        s = uniform_down_sample(s, ds_rate)
    t = copy.deepcopy(gt_target)
    t = crop_volume.crop_point_cloud(t)
    #t = VoxelDownSample(t, voxel_size)
    t_len = len(t.points)
    if(t_len>max_size):
        ds_rate = int(round(t_len/float(max_size)))
        t = uniform_down_sample(t, ds_rate)
#	if new_o3d_flag:
#		reg = registration_icp(s, t, threshold, np.identity(4), TransformationEstimationPointToPoint(True), ICPConvergenceCriteria(1e-6, max_itr))
#    else:
#        reg = registration_icp(s, t, threshold, np.identity(4), TransformationEstimationPointToPoint(True), ConvergenceCriteria(1e-6, max_itr))
#
    reg = registration_icp(s, t, threshold, np.identity(4), TransformationEstimationPointToPoint(True), ICPConvergenceCriteria(1e-6, max_itr))
    print("reg init:", init_trans)
    print("reg icp:", reg.transformation)
    reg.transformation = np.matmul(reg.transformation, init_trans)
    print("reg icp corr.:", reg.transformation)
    return reg

def registration_vol_ds(source, gt_target, init_trans, crop_volume, voxel_size, threshold, max_itr):
    set_verbosity_level(VerbosityLevel.Debug)
    s = copy.deepcopy(source)
    s.transform(init_trans)
    s = crop_volume.crop_point_cloud(s)
    s = voxel_down_sample(s, voxel_size)

    t = copy.deepcopy(gt_target)
    t = crop_volume.crop_point_cloud(t)
    t = voxel_down_sample(t, voxel_size)

    reg = registration_icp(s, t, threshold, np.identity(4), TransformationEstimationPointToPoint(True), ICPConvergenceCriteria(1e-6, max_itr))
    print("reg init:", init_trans)
    print("reg icp:", reg.transformation)
    reg.transformation = np.matmul(reg.transformation, init_trans)
    print("reg icp corr.:", reg.transformation)
    return reg
