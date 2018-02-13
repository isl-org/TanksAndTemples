import numpy as np
import numpy.linalg
import sys
from setup_open3d import *

import numpy as np

from trajectory_io import *
from registration import *
from evaluation import *
from util import *
from plot import *


dTau_dict = {"Barn":0.01,"Caterpillar":0.005,"Church":0.025,"Courthouse":0.025,"Ignatius":0.003, "Meetingroom":0.01,"Truck":0.005}

scenes = ["Barn","Caterpillar","Church","Courthouse","Ignatius", "Meetingroom","Truck"]
#taus =[0.01,0.005,0.015,0.02,0.003,0.01,0.005]
scenes = ["Barn","Caterpillar","Ignatius", "Meetingroom","Truck"]
#taus =[0.01,0.005,0.003,0.01,0.005]
scenes = ["Church","Courthouse"]
scenes = ["Barn","Caterpillar","Church","Courthouse","Ignatius", "Meetingroom","Truck"]
eva_list = []


for scene in scenes:

	dTau = dTau_dict[scene]
	#scene = "Ignatius"
	# put the crop-file, the GT file, the COLMAP SfM log file and the alignment of the according scene in a folder of the same scene name in the base_dir
	base_dir = "/Users/jaesikpa/Research/TanksAndTemples/evaluation/"
	mvs_outpath = base_dir + scene + '/evaluation/'

	make_dir(mvs_outpath)

	sfm_dirname = base_dir + scene + "/"
	colmap_ref_logfile = sfm_dirname + scene + '_COLMAP_SfM.log'
	alignment = sfm_dirname + scene + '_trans.txt'
	gt_filen = base_dir + scene + '/' + scene + '.ply'
	cropfile = base_dir + scene + '/' + scene + '.json'


	###############################################################
	# User input files:
	# SfM log file and pointcoud of your reconstruction comes here.
	# as an example the COLMAP data will be used, but the script
	# should work with any other method as well
	###############################################################
	new_logfile = sfm_dirname + scene + '_COLMAP_SfM.log'
	mvs_file = base_dir + scene + '/' + scene + '_COLMAP.ply'

	#Load reconstruction and according GT
	pcd = read_point_cloud(mvs_file)
	gt_pcd = read_point_cloud(gt_filen)


	gt_trans = np.loadtxt(alignment)


	traj_to_register = read_trajectory(new_logfile)


	gt_traj_col = read_trajectory(colmap_ref_logfile)
	#gt_trans = read_alignment_transformation(alignment)


	traj_pcd_col = convert_trajectory_to_pointcloud(gt_traj_col)
	traj_pcd_col.transform(gt_trans)

	corres = Vector2iVector(np.asarray(list(map(lambda x: [x, x], range(len(gt_traj_col))))))

	rr=RANSACConvergenceCriteria()
	rr.max_iteration = 100000
	rr.max_validation = 100000

	if len(traj_to_register) > 1600:  #in this case a log file was used which contains every movie frame (see tutorial for details)
		traj_col2 = gen_sparse_trajectory(mapping, traj_to_register)
		traj_to_register_pcd = convert_trajectory_to_pointcloud(traj_col2)
	else:
		traj_to_register_pcd = convert_trajectory_to_pointcloud(traj_to_register)


	#randomvar = 0.05 # 5% error added
	randomvar = 0.0

	nr_of_cam_pos = len(traj_to_register_pcd.points)
	rand_number_added = np.asanyarray(traj_to_register_pcd.points)*(np.random.rand(nr_of_cam_pos,3)*randomvar-randomvar/2.0+1)
	list_rand = list(rand_number_added)
	traj_to_register_pcd_rand = PointCloud()
	for elem in list_rand:
		traj_to_register_pcd_rand.points.append(elem)
		# Rough registration based on aligned colmap SfM data
		#reg = registration_ransac_based_on_correspondence(traj_to_register_pcd, traj_pcd_col, corres, 0.2, TransformationEstimationPointToPoint(True),6, rr)
		reg = registration_ransac_based_on_correspondence(traj_to_register_pcd_rand, traj_pcd_col, corres, 0.2, TransformationEstimationPointToPoint(True),6, rr)


		# Refine alignment by using the actual GT and MVS pointclouds
		vol = read_selection_polygon_volume(cropfile)
		maxsize = 1e6 # big pointclouds will be downlsampled to this number to speed up alignment
		dist_threshold = dTau

		# original
		# #Registration refinment in 3 iterations, should be possible to do it in 2? Could be faster
		# r2  = registration_vol_ds(pcd, gt_pcd, reg.transformation, vol, 3*dTau, dTau*120, 20)
		# r3  = registration_vol_ds(pcd, gt_pcd, r2.transformation, vol, 2*dTau, dTau*30, 20)
		# #r  = registration_vol_ds(pcd, gt_pcd, r3.transformation, vol, dTau, dTau*15, 20)
		# r  = registration_unif(pcd, gt_pcd, r3.transformation, vol, dTau*15, 20, 4*maxsize)

		# test
		r  = registration_vol_ds(pcd, gt_pcd, reg.transformation, vol, 3*dTau, dTau*120, 20)


		# Histogramms and P/R/F1
		plot_stretch = 5
		[precision, recall, fscore, edges_source, cum_source, edges_target, cum_target] = EvaluateHisto(pcd, gt_pcd, r.transformation, vol, dTau/2.0, dTau, mvs_outpath, plot_stretch, scene)
		eva = [precision, recall, fscore]
		eva_list.append(eva)
		print("==============================")
		print("evaluation result : %s" % scene)
		print("==============================")
		print("distance tau : %.3f" % dTau)
		print("precision : %.4f" % eva[0])
		print("recall : %.4f" % eva[1])
		print("f-score : %.4f" % eva[2])
		print("==============================")


		# Plotting
		plot_graph(fscore, edges_source, cum_source, edges_target, cum_target)
