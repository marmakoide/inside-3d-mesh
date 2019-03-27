import sys
import numpy

import stlparser

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D



# Compute euclidean norm along axis 1
def anorm2(X):
	return numpy.sqrt(numpy.sum(X ** 2, axis = 1))



# Compute 3x3 determinnant along axis 1
def adet(X, Y, Z):
	ret  = numpy.multiply(numpy.multiply(X[:,0], Y[:,1]), Z[:,2])
	ret += numpy.multiply(numpy.multiply(Y[:,0], Z[:,1]), X[:,2])
	ret += numpy.multiply(numpy.multiply(Z[:,0], X[:,1]), Y[:,2])
	ret -= numpy.multiply(numpy.multiply(Z[:,0], Y[:,1]), X[:,2])
	ret -= numpy.multiply(numpy.multiply(Y[:,0], X[:,1]), Z[:,2])
	ret -= numpy.multiply(numpy.multiply(X[:,0], Z[:,1]), Y[:,2])
	return ret



def is_inside(triangles, X):
	# One generalized winding number per input vertex
	ret = numpy.zeros(X.shape[0])
	
	# Acuumulate generalized winding number for each triangle
	for U, V, W in triangles:	
		A, B, C = U - X, V - X, W - X
		omega = adet(A, B, C)

		a, b, c = anorm2(A), anorm2(B), anorm2(C)
		k  = a * b * c 
		k += c * numpy.sum(numpy.multiply(A, B), axis = 1)
		k += a * numpy.sum(numpy.multiply(B, C), axis = 1)
		k += b * numpy.sum(numpy.multiply(C, A), axis = 1)

		ret += numpy.arctan2(omega, k)

	# Job done
	return ret >= 2 * numpy.pi 



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
	P = (max_corner - min_corner) * numpy.random.random((8198, 3)) + min_corner

	# Filter out points which are not inside the mesh
	P = P[is_inside(triangles, P)]

	# Display
	fig = plot.figure()
	ax = fig.gca(projection = '3d')
	ax.set_aspect('equal')
	ax.scatter(P[:,0], P[:,1], P[:,2], lw = 0., c = 'k')
	plot.show()
	


if __name__ == '__main__':
	main()
