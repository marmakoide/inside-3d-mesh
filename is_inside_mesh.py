import numpy



'''
Naive and straightforward implementation of the inside/outside point mesh test
'''

def is_inside_naive(triangles, X):
	# Compute triangle vertices and their norms relative to X
	M = triangles - X
	M_norm = numpy.sqrt(numpy.sum(M ** 2, axis = 2))

	# Accumulate generalized winding number per triangle
	winding_number = 0.
	for (A, B, C), (a, b, c) in zip(M, M_norm):
		winding_number += numpy.arctan2(numpy.linalg.det(numpy.array([A, B, C])), (a * b * c) + c * numpy.dot(A, B) + a * numpy.dot(B, C) + b * numpy.dot(C, A))

	# Job done
	return winding_number >= 2. * numpy.pi



'''
Optimized for numpy implementation of the inside/outside point mesh test
'''

# Compute euclidean norm along axis 1
def anorm2(X):
	return numpy.sqrt(numpy.sum(X ** 2, axis = 1))



# Compute 3x3 determinant along axis 1
def adet(X, Y, Z):
	ret  = numpy.multiply(numpy.multiply(X[:,0], Y[:,1]), Z[:,2])
	ret += numpy.multiply(numpy.multiply(Y[:,0], Z[:,1]), X[:,2])
	ret += numpy.multiply(numpy.multiply(Z[:,0], X[:,1]), Y[:,2])
	ret -= numpy.multiply(numpy.multiply(Z[:,0], Y[:,1]), X[:,2])
	ret -= numpy.multiply(numpy.multiply(Y[:,0], X[:,1]), Z[:,2])
	ret -= numpy.multiply(numpy.multiply(X[:,0], Z[:,1]), Y[:,2])
	return ret



def is_inside_turbo(triangles, X):
	# One generalized winding number per input vertex
	ret = numpy.zeros(X.shape[0])
	
	# Accumulate generalized winding number for each triangle
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

