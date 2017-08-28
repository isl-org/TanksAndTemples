#!/usr/bin/env python
#
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
# Python script to convert COLMAP SfM data into the tanksandtempls log file format
# Example: python get_mve_SfM_logfile.py [MVE SfM file] [output log-filename] [folder containing the mve views]

import sys
import glob
import numpy as np
from numpy import matrix

def write_trajectory(traj, filename):
    with open(filename, 'w') as f:
        for x in traj:
            p = x.pose.tolist()
            f.write(' '.join(map(str, x.metadata)) + '\n')
            f.write('\n'.join(' '.join(map('{0:.12f}'.format, p[i])) for i in range(4)))
            f.write('\n')
            
            
def write_SfM_log(T, i_map, filename):
    with open(filename, 'w') as f:
        ii=0
        for t in T:
            p = t.tolist()
            f.write(' '.join(map(str, i_map[ii])) + '\n')
            f.write('\n'.join(' '.join(map('{0:.12f}'.format, p[i])) for i in range(4)))
            f.write('\n')
            ii = ii + 1
                        
                        
  


def convert_to_log(argv):
	
	filename = argv[1] 
	logfile_out = argv[2] 
	views_folder = argv[3]

	bundlefile = filename
	lines = open(bundlefile).read().split('\n')
	views_list = glob.glob(views_folder + '/*/')
	views_list.sort()
	nr_of_views = len(views_list)
	nr_of_images = int(lines[1].split(' ')[0])

	R = []
	t = []
	T = []
	i_map = []
	TF = []
	i_mapF = []

	image_list = []
	ii=0

	for x in range(0, nr_of_views):
		
		meta_filename = views_list[x]+'meta.ini'
		lines_m = open(meta_filename).read().split('\n')
		matching_i = [i for i,s in enumerate(lines_m) if 'name = ' in s]
		orig_img = lines_m[matching_i[0]].split('= ')[1]
		image_list.append(orig_img)

	image_list.sort()	

	for x in range(0, nr_of_views):
		
		meta_filename = views_list[x]+'meta.ini'
		lines_m = open(meta_filename).read().split('\n')
		matching_r = [i for i,s in enumerate(lines_m) if 'rotation' in s]
		
		if(len(matching_r)):
			r_line = lines_m[matching_r[0]].split('= ')[1]
			r = np.array(r_line.split(' '),dtype='double').reshape(3,3)	
			matching_t = [i for i,s in enumerate(lines_m) if 'translation' in s]
			t_line = lines_m[matching_t[0]].split('= ')[1]
			t1 = np.array(t_line.split(' ')[0:3],dtype='double')
			R.append(r)
			t.append(t1)
			w = np.zeros((4,4))
			w[3,3] = 1
			w[0:3,0:3]=r
			w[0:3,3]=t1 
			A = matrix(w)
			T.append(A.I)
			matching_i = [i for i,s in enumerate(lines_m) if 'name = ' in s]
			orig_img = lines_m[matching_i[0]].split('= ')[1]
			matching_io = [i for i,s in enumerate(image_list) if orig_img in s]
			i_map.append(np.array([x,matching_io[0],0.0],dtype='int'))	
			
	idm = np.identity(4)
	ww=np.array(i_map).tolist()	
	
	# log file needs an entry for every input image, if image is not part of the SfM bundle it will be assigned to the identity matrix
	for k in range(0,nr_of_images):
		
		try:
			bundler_id = [i for i, item in enumerate(ww) if k==item[1]][0] # find the bundler id of view nr. k
			i_mapF.append(np.array([k,k,0.0],dtype='int'))	
			TF.append(T[bundler_id])
		except:
			i_mapF.append(np.array([k,-1,0.0],dtype='int'))	
			TF.append(idm)
	write_SfM_log(TF, i_mapF, logfile_out)
	
	
if __name__ == '__main__':
    convert_to_log(sys.argv)

