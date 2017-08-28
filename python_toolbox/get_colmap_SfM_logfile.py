#!/usr/bin/env python
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

	



def convert_to_log(args):
	
	filename = sys.argv[1] 
	logfile_out = sys.argv[2] 
	input_images = sys.argv[3]
	formatp = sys.argv[4]
	lines = open(filename).read().split('\n')
	nr_of_views = int(len(lines)-5)/2
	jpg_list = glob.glob(input_images+'/*.'+formatp)
	jpg_list.sort()
	nr_of_images = len(jpg_list)

	R = []
	t = []
	T = []
	i_map = []
	TF = []
	i_mapF = []


	ii=0
	for x in range(4, int(nr_of_views*2+4),2):
		line_split = lines[x].split(' ')
		qvec = np.array([float(line_split[1]), float(line_split[2]), float(line_split[3]), float(line_split[4])])
		r = quat2rotmat(qvec)
		t1 = np.array([float(line_split[5]), float(line_split[6]), float(line_split[7])])
		R.append(r)
		t.append(t1)
		w = np.zeros((4,4))
		w[3,3] = 1
		w[0:3,0:3]=r
		w[0:3,3]=t1 
		A = matrix(w)
		T.append(A.I)
		image_name = line_split[9]
		matching = [i for i,s in enumerate(jpg_list) if image_name in s]
		ii = int(line_split[0])-1
		i_map.append(np.array([ii,matching[0],0.0],dtype='int'))	

	ww=np.array(i_map).tolist()	
	idm = np.identity(4)

	# log file needs an entry for every input image, if image is not part of the SfM bundle it will be assigned to the identity matrix
	for k in range(0,nr_of_images):
		
		try:
			bundler_id = [i for i, item in enumerate(ww) if k==item[1]][0] # find the id of view nr. k
			i_mapF.append(np.array([k,k,0.0],dtype='int'))	
			TF.append(T[bundler_id])
		except:
			i_mapF.append(np.array([k,-1,0.0],dtype='int'))	
			TF.append(idm)
				
	write_SfM_log(TF, i_mapF, logfile_out)

if __name__ == '__main__':
    convert_to_log(sys.argv[1:])
