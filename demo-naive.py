import sys
import numpy

import stlparser

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D



def is_inside(triangles, X):
	# Compute triangle vertices and their norms relative to X
	M = triangles - X
	M_norm = numpy.sqrt(numpy.sum(M ** 2, axis = 2))

	# Accumulate generalized winding number per triangle
	winding_number = 0.
	for (A, B, C), (a, b, c) in zip(M, M_norm):
		winding_number += numpy.arctan2(numpy.linalg.det(numpy.array([A, B, C])), (a * b * c) + c * numpy.dot(A, B) + a * numpy.dot(B, C) + b * numpy.dot(C, A))

	# Job done
	return winding_number >= 2. * numpy.pi


def main():
	# Load the input mesh as a list of triplets (ie. triangles) of 3d vertices
	try:
		triangles = numpy.array([X for X, N in stlparser.load(sys.stdin)])
	except stlparser.ParseError as e:
		sys.stderr.write('%s\n' % e)
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
	ax.set_aspect('equal')
	ax.scatter(P[:,0], P[:,1], P[:,2], lw = 0., c = 'k')
	plot.show()



if __name__ == '__main__':
	main()
