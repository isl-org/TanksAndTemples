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
# Python script to convert VSfM SfM data into the tanksandtempls log file format
# Example: python get_colmap_SfM_logfile.py [VSfM *.nvm SfM file] [output log-filename] [folder of the input images] [image format]

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
   
   
                        
                        
def quat2rotmat(qvec):

	rotmat = np.array([1- 2 * qvec[2]**2 - 2 * qvec[3]**2, \
	2 * qvec[1] * qvec[2] - 2 * qvec[0] * qvec[3], \
	2 * qvec[3] * qvec[1] + 2 * qvec[0] * qvec[2], \
	\
	2 * qvec[1] * qvec[2] + 2 * qvec[0] * qvec[3], \
	1 - 2 * qvec[1]**2 - 2 * qvec[3]**2, \
	2 * qvec[2] * qvec[3] - 2 * qvec[0] * qvec[1], \
	\
	2 * qvec[3] * qvec[1] - 2 * qvec[0] * qvec[2], \
	2 * qvec[2] * qvec[3] + 2 * qvec[0] * qvec[1], \
	1 - 2 * qvec[1]**2 - 2 * qvec[2]**2])
	rotmat = rotmat.reshape(3,3)
	return rotmat



def convert_to_log(argv):
	
	filename = argv[1] 
	logfile_out = argv[2] 
	input_images = argv[3]
	formatp = argv[4]

	bundlefile = filename
	lines = open(bundlefile).read().split('\n')
	nr_of_views = int(lines[2])
	jpg_list = glob.glob(input_images+'/*.'+formatp)
	jpg_list.sort()
	nr_of_images = len(jpg_list)

	R = []
	t = []
	tx = []
	T = []
	i_map = []
	TF = []
	i_mapF = []
	ii=0

	for x in range(3, nr_of_views+3):
		line_split = lines[x].split(' ')
		qvec = np.array([float(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4])])
		r = quat2rotmat(qvec)
		t1x = np.array([float(line_split[5]), float(line_split[6]), float(line_split[7])])
		tx.append(t1x)
		r = r*np.array([[1],[-1],[-1]]) # no idea why this is necessary 
		t1 = np.dot(-r,t1x)
		R.append(r)
		t.append(t1)
		w = np.zeros((4,4))
		w[3,3] = 1
		w[0:3,0:3]=r
		w[0:3,3]=t1 
		A = matrix(w)
		T.append(A.I)
		image_name = line_split[0].split('\t')[0]
		matching = [i for i,s in enumerate(jpg_list) if image_name in s]
		ii = x-3
		i_map.append(np.array([ii,matching[0],0.0],dtype='int'))	
	idm = np.identity(4)

	ww=np.array(i_map).tolist()	
	
	# log file needs an entry for every input image, if image is not part of the SfM bundle it will be assigned to the identity matrix
	for k in range(0,nr_of_images):
		
		try:
			bundler_id = [i for i, item in enumerate(ww) if k==item[1]][0] # find the bundler id of view nr. k
			i_mapF.append(np.array([k,bundler_id,0.0],dtype='int'))	
			TF.append(T[bundler_id])
		except:
			i_mapF.append(np.array([k,-1,0.0],dtype='int'))	
			TF.append(idm)
				
	write_SfM_log(TF, i_mapF, logfile_out)	
	
if __name__ == '__main__':
    convert_to_log(sys.argv)
