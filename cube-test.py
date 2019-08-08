import numpy
from is_inside_mesh import is_inside_turbo as is_inside

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D



def is_inside_cube(cube_size, X):
	return numpy.amax(numpy.fabs(X), axis = 1) < (cube_size / 2)



def main():
	# Input mesh is a cube of size 1 and centered on (0, 0, 0)
	triangles = numpy.array([
		[[-.5,  .5, -.5],
		 [ .5,  .5,  .5],
		 [ .5,  .5, -.5]],
		[[-.5,  .5, -.5],
		 [-.5,  .5,  .5],
		 [ .5,  .5,  .5]],
		[[-.5, -.5, -.5],
		 [-.5, -.5,  .5],
		 [-.5,  .5, -.5]],  
		[[-.5, -.5,  .5],
		 [-.5,  .5,  .5],
		 [-.5,  .5, -.5]],
		[[-.5, -.5, -.5],
		 [ .5, -.5, -.5],
		 [-.5, -.5,  .5]],
		[[ .5, -.5, -.5],
		 [ .5, -.5,  .5],
		 [-.5, -.5,  .5]],   
		[[ .5, -.5, -.5],
		 [ .5,  .5, -.5],
		 [ .5,  .5,  .5]],
		[[ .5, -.5, -.5],
		 [ .5,  .5,  .5],
		 [ .5, -.5,  .5]],
		[[-.5, -.5,  .5],
		 [ .5, -.5,  .5],
		 [ .5,  .5,  .5]],
		[[-.5, -.5,  .5],
		 [ .5,  .5,  .5],
		 [-.5,  .5,  .5]],
		[[-.5, -.5, -.5],
		 [-.5,  .5, -.5],
		 [ .5, -.5, -.5]],
		[[ .5, -.5, -.5],
		 [-.5,  .5, -.5],
		 [ .5,  .5, -.5]]])
	
	# Compute uniform distribution that fits in a cube of size 2 and centered on (0, 0, 0)
	P = 2 * (numpy.random.random((4096, 3)) - .5)
	P = P.astype('longdouble')

	# Test each point using the point in cube test
	P_inside_cube = is_inside_cube(1, P)
	
	# Test each point using the point-in-mesh test
	P_inside_mesh = is_inside(triangles, P)

	# Print statistics on the difference between the two tests
	positive_count = sum(P_inside_cube)
	negative_count = sum(~P_inside_cube)

	true_positive_count = sum(P_inside_cube & P_inside_mesh)
	false_positive_count = sum(~P_inside_cube & P_inside_mesh)
	true_negative_count = sum(~P_inside_cube & ~P_inside_mesh)
	false_negative_count = sum(P_inside_cube & ~P_inside_mesh)

	print(f'point correctly tested as inside = {true_positive_count}/{positive_count})')
	print(f'point incorrectly tested as inside = {false_positive_count}/{positive_count})')
	print(f'point correctly tested as outside = {true_negative_count}/{negative_count})')
	print(f'point incorrectly tested as outside = {false_negative_count}/{negative_count})')




if __name__ == '__main__':
	main()
