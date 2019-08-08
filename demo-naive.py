import sys
import numpy

import stlparser
from is_inside_mesh import is_inside_naive as is_inside

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D



def main():
	# Load the input mesh as a list of triplets (ie. triangles) of 3d vertices
	try:
		triangles = numpy.array([X for X, N in stlparser.load(sys.stdin)])
	except stlparser.ParseError as e:
		sys.stderr.write(f'{e}\n')
		sys.exit(0)
	
	# Compute uniform distribution within the axis-aligned bound box for the mesh
	min_corner = numpy.amin(numpy.amin(triangles, axis = 0), axis = 0)
	max_corner = numpy.amax(numpy.amax(triangles, axis = 0), axis = 0)
	P = (max_corner - min_corner) * numpy.random.random((4096, 3)) + min_corner

	# Filter out points which are not inside the mesh
	P = numpy.array([p for p in P if is_inside(triangles, p)])
	
	# Display the points in/out the mesh
	fig = plot.figure()
	ax = fig.gca(projection = '3d')
	ax.scatter(P[:,0], P[:,1], P[:,2], lw = 0., c = 'k')
	plot.show()



if __name__ == '__main__':
	main()
