import json
import copy
import numpy as np
from setup_open3d import *

def read_alignment_transformation(filename):
	with open(filename) as data_file:
		data = json.load(data_file)
	return np.asarray(data['transformation']).reshape((4, 4)).transpose()


def EvaluateHisto(source, target, trans, crop_volume, voxel_size, threshold, filename_mvs, plot_stretch, scene_name):

	set_verbosity_level(VerbosityLevel.Debug)
	s = copy.deepcopy(source)
	s.transform(trans)
	s = crop_volume.crop_point_cloud(s)
	s = voxel_down_sample(s, voxel_size)
	print(filename_mvs+"/" + scene_name + ".precision.ply")
#	write_point_cloud(filename_mvs+"/" + scene_name + ".precision.ply", s)
#	write_point_cloud(filename_mvs+"/" + scene_name + ".precision.ncb.ply", s)
#
	t = copy.deepcopy(target)
	t = crop_volume.crop_point_cloud(t)
	t = voxel_down_sample(t, voxel_size)
#	write_point_cloud(filename_mvs+"/" + scene_name + ".recall.ply", t)

	distance1 = compute_point_cloud_to_point_cloud_distance(s, t)
	distance2 = compute_point_cloud_to_point_cloud_distance(t, s)


#   # write the distances to bin files
#	np.array(distance1).astype('float64').tofile(filename_mvs+"/" + scene_name + ".precision.bin")
#	np.array(distance2).astype('float64').tofile(filename_mvs+"/" + scene_name + ".recall.bin")

# bin_dir = '/Users/jaesikpa/Research/Open3D/build/bin/'
# import os

#   #############################################################################
#   # Colorize the poincloud files prith the precision and recall values
#   #############################################################################
#	write_point_cloud(filename_mvs+"/" + scene_name + ".precision.ply", s)
#	write_point_cloud(filename_mvs+"/" + scene_name + ".precision.ncb.ply", s)
#
#	write_point_cloud(filename_mvs+"/" + scene_name + ".recall.ply", t)

#    knn = 20
#	target_n_fn_knn = filename_mvs + "/" + scene_name + ".recall_" + str(knn) + ".ply"
#	source_n_fn_knn = filename_mvs + "/" + scene_name + ".precision_" + str(knn) + ".ply"
#
#	source_n_fn = filename_mvs + "/" + scene_name + ".precision.ply"
#	#source_ncb_fn = filename_mvs + "/alignment.source.ncb.ply"
#	target_n_fn = filename_mvs + "/" + scene_name + ".recall.ply"
#
#	eval_str_viewDT = bin_dir + "ViewDistances " + source_n_fn + " --max_distance " + str(threshold*3) + " --write_color_back --without_gui"
#	os.system(eval_str_viewDT)
#
#
#
#	eval_str_viewDT = bin_dir + "ViewDistances " + target_n_fn + " --max_distance " + str(threshold*3) + " --write_color_back --without_gui"
#	os.system(eval_str_viewDT)
#
#
#
#	eval_str_convert_n_s = bin_dir + "ConvertPointCloud " + source_n_fn + " " + source_n_fn_knn + " --estimate_normals_knn " + str(knn)
#	print(eval_str_convert_n_s)
#	os.system(eval_str_convert_n_s)
#
#	eval_str_convert_n_t = bin_dir + "ConvertPointCloud " + target_n_fn + " " + target_n_fn_knn + " --estimate_normals_knn " + str(knn)
#	print(eval_str_convert_n_t)
#	os.system(eval_str_convert_n_t)
#
#
#


	[precision, recall, fscore, edges_source, cum_source, edges_target, cum_target] = get_f1_score_histo2(threshold, filename_mvs, plot_stretch, distance1, distance2)
	np.savetxt(filename_mvs+"/" + scene_name + ".recall.txt",cum_target)
	np.savetxt(filename_mvs+"/" + scene_name + ".precision.txt",cum_source)
	np.savetxt(filename_mvs+"/" + scene_name + ".prf_tau_plotstr.txt",np.array([precision, recall, fscore, threshold, plot_stretch]))


	return [precision, recall, fscore, edges_source, cum_source, edges_target, cum_target]


def get_f1_score_histo2(threshold, filename_mvs, plot_stretch, distance1, distance2):
	# plot_stretch = 5

	dist_threshold = threshold
	if(len(distance1) and len(distance2)):

		recall = float(sum(d < threshold for d in distance2)) / float(len(distance2))
		precision = float(sum(d < threshold for d in distance1)) / float(len(distance1))
		fscore = 2 * recall * precision / (recall + precision)
		num = len(distance1)
		bins = np.arange(0, dist_threshold*plot_stretch , dist_threshold / 100)
		hist, edges_source = np.histogram(distance1, bins)
		cum_source = np.cumsum(hist).astype(float) / num


		num = len(distance2)
		bins = np.arange(0, dist_threshold*plot_stretch , dist_threshold / 100)
		hist, edges_target = np.histogram(distance2, bins)
		cum_target = np.cumsum(hist).astype(float) / num

	else:
		precision = 0
		recall = 0
		fscore = 0
		edges_source = np.array([0])
		cum_source = np.array([0])
		edges_target = np.array([0])
		cum_target = np.array([0])

	return [precision, recall, fscore, edges_source, cum_source, edges_target, cum_target] #source = precission, target = recall
