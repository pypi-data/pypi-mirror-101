import numpy as np
from scipy import linalg

def identity(shape):
	return Matrix(np.identity(shape,dtype = int))

def null(shape):
	return Matrix(np.zeros(shape,dtype=int))

class Matrix:
	"""
	This is a Class of Matrix.
	It takes a python list as an argument.
	We can do all kinds of operations that are to be done on a Matrix.
	Operations we can do are:
		1. Addition/Subtraction of two Matrices
		2. Muliplication/Division of Two Matrices
		3. Multiplication/Division of A Matrix by a Scaler
		4. Power of Matrix to an Integer
		5. Transpose of a Matrix
		6. Determinant of a Matrix
		7. Minors/Cofactors of element in the matrix
		8. Cofactor Matrix of a Matrix
		8. Adjoint/Inverse of a Matrix
		9. Drop a Row/Column in a Matrix
		10.Trace of Matrix

	We can check whether the given Matrix:
		 is_symmetric
		 is_skew_symmetric
		 is_orthogonal
		 is_upper
		 is_lower
		 is_diagonal
		 is_identity
		 is_vertical
		 is_horizontal
		 is_scaler
	"""
	def __init__(self,matrix):
		self.matrix = np.array(matrix)
		self.shape = self.matrix.shape
		self.dtype = self.matrix.dtype

	def __getitem__(self,index):
		"""
		gets the item of specified index
		"""
		return self.matrix[index]

	def __add__(self,other):
		"""
		simply adds two matrices of same shape element by element
		"""
		if type(other) == type(self):
			if self.shape == other.shape:
				return Matrix(np.add(self.matrix,other.matrix))
			raise ValueError(f"operands could not use '+' with shapes {self.shape} {other.shape}")
		raise TypeError(f"cannot use '+' operation between operands {type(self).__name__} and {type(other).__name__}")

	def __sub__(self,other):
		"""
		simply subtracts two matrices of same shape element by element
		"""
		if type(other) == type(self):
			if self.matrix.shape == other.matrix.shape:
				return Matrix(np.add(self.matrix,-1*other.matrix))
			raise ValueError(f"operands could not use '-' with shapes {self.shape} {other.shape}")
		raise TypeError(f"cannot use '-' operation between operands {type(self).__name__} and {type(other).__name__}")

	def __mul__(self,other):
		"""
		if both the operands are matrices and obeys the matrix functionality for multiplication then it simply multiplies two matrices
		if one operand is an integer or float then there will be a scalar multiplication.
		"""
		if type(other) == int or type(other) == float:
			result = self.matrix
			if type(other) == float:
				result = self.matrix.astype('float64')
			for i in range(self.shape[0]):
				for j in range(self.shape[1]):
					result[i][j] *= other
			return Matrix(result)
		elif type(other) == type(self):
			if self.shape[1] == other.shape[0]:
				result = np.array([0.0]*(self.matrix.shape[0]*other.matrix.shape[1])).reshape(self.matrix.shape[0],other.matrix.shape[1])
				for i in range(self.matrix.shape[0]):
					for j in range(other.matrix.shape[1]):
						for k in range(self.matrix.shape[1]):
							result[i][j] += self.matrix[i][k] * other.matrix[k][j]
				return Matrix(result)
			raise ValueError(f"operands could not use '*' with shapes {self.shape} {other.shape}")
		raise TypeError(f"cannot use '*' operation between operands {type(self).__name__} and {type(other).__name__}")

	def __rmul__(self,other):
		if type(other) == int or type(other) == float:
			result = self.matrix
			if type(other) == float:
				result = self.matrix.astype('float64')
			for i in range(self.shape[0]):
				for j in range(self.shape[1]):
					result[i][j] *= other
			return Matrix(result)
		raise TypeError(f"cannot use '*' operation between operands {type(other).__name__} and {type(self).__name__}")

	def __truediv__(self,other):
		if type(other) == int or type(other) == float:
			result = self.matrix.astype('float64')
			for i in range(self.shape[0]):
				for j in range(self.shape[1]):
					result[i][j] /= other
			return Matrix(result)
		elif type(other) == type(self):
			if (other.shape[0] == other.shape[1]) and (self.shape[1] == other.shape[0]): 
				return Matrix(self.matrix.astype('float64')) * (Matrix(other.matrix).inverse())
			raise ValueError(f"operands could not use '/' with shapes {self.shape} {other.shape}")
		raise TypeError(f"cannot use '/' operation between operands {type(self).__name__} and {type(other).__name__}")

	def __rtruediv__(self,other):
		if type(other) == int or type(other) == float:
			return other*self.inverse()
		raise TypeError(f"cannot use '/' operation between operands {type(other).__name__} and {type(self).__name__}")		

	def __pow__(self,integer):
		if type(integer) == int:
			if self.shape[0] == self.shape[1]:
				if integer == 0:
					return Matrix(np.identity(self.shape[0]))
				elif integer > 0:
					result = Matrix(np.identity(self.shape[0]))
					for _ in range(integer):
						result *= Matrix(self.matrix)
					return result
				else:
					if integer == -1:
						return self.inverse()
					else:
						return self.inverse()**((-1)*integer)
			raise ValueError(f"The shape {self.shape} is not a shape of square matrix")
		raise TypeError("The power must be an integer.")

	def __eq__(self,other):
		if type(other) == type(self):
			if self.shape == other.shape:
				for i in range(self.shape[0]):
					for j in range(self.shape[1]):
						if self[i][j] != other[i][j]:
							return False
				return True
			return False
		raise TypeError(f"cannot use '==' operation between operands {type(self).__name__} and {type(other).__name__}")

	def __neg__(self):
		return -1 * self

	def __pos__(self):
		return self

	def trace(self):
		"""
		arguments:
			None
		returns:
			trace of the matrix: int
		"""
		if self.shape[0] == self.shape[1]:
			trace = 0
			for i in range(self.shape[0]):
				trace += self[i][i]
			return trace
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def T(self):
		"""
		arguments:
			None
		returns:
			transpose of the matrix: Matrix
		"""
		return Matrix(self.matrix.transpose())

	def det(self):
		"""
		arguments:
			None
		returns:
			determinant of the matrix: int/float
		"""
		if self.shape[0] == self.shape[1]:
			return linalg.det(self.matrix)
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def drop_row(self,row):
		"""
		arguments:
			row: int
		returns:
			matrix with row dropped: Matrix
		"""
		return Matrix(np.concatenate((self.matrix[:row],self.matrix[row+1:]),axis = 0))

	def drop_column(self,column):
		"""
		arguments:
			column: int
		returns:
			matrix with column dropped: Matrix
		"""
		return Matrix(np.concatenate((self.matrix[:,:column],self.matrix[:,column+1:]),axis = 1))

	def minor(self,row,column):
		"""
		arguments:
			row: int
			column: int
		returns:
			matrix with column and row dropped: Matrix
		"""
		element = self.matrix[row][column]
		if row >= self.shape[0] or column >= self.shape[1]:
			raise IndexError(f"{row}, {column} index out of range.")
		if self.shape[0] == self.shape[1]:
			A = Matrix(self.matrix)
			A = A.drop_row(row)
			A = A.drop_column(column)
			return A
		else:
			raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def cofactor(self,row,column):
		"""
		arguments:
			row: int
			column: int
		returns:
			cofactor of the element in the row and column: int/float
		"""
		return (self.minor(row,column).det())*((-1)**(row + column))

	def cofactor_matrix(self):
		"""
		arguments:
			None
		returns:
			cofactor matrix: Matrix
		"""
		if self.shape[0] == self.shape[1]:
			result = np.zeros(self.shape)
			for i in range(self.shape[0]):
				for j in range(self.shape[0]):
					result[i][j] = self.cofactor(i,j)
			return Matrix(result)
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def adjoint(self):
		"""
		arguments:
			None
		returns:
			adjoint matrix: Matrix
		"""
		return self.cofactor_matrix().T()

	def inverse(self):
		"""
		arguments:
			None
		returns:
			inverse matrix: Matrix
		"""
		A = Matrix(self.matrix.astype('float64'))
		B = A.adjoint()
		if A.det() != 0:
			return B/(A.det())
		raise ZeroDivisionError('Cannot divide by zero')
		
	#################################################################
	# checks of matrix
	#################################################################

	def is_symmetric(self):
		if self.shape[0] == self.shape[1]:
			return self.T() == self
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def is_skew_symmetric(self):
		if self.shape[0] == self.shape[1]:
			return self.T() == -self
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def is_orthogonal(self):
		if self.shape[0] == self.shape[1]:
			return self.T() == self.inverse()
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def is_upper(self):
		if self.shape[0] == self.shape[1]:
			for i in range(1,self.shape[0]):
				for j in range(self.shape[0]-1):
					if i>j:
						if self[i][j] != 0:
							return False
			return True
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def is_lower(self):
		if self.shape[0] == self.shape[1]:
			for i in range(self.shape[0]-1):
				for j in range(1,self.shape[0]):
					if i<j:
						if self[i][j] != 0:
							return False
			return True
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def is_diagonal(self):
		if self.shape[0] == self.shape[1]:
			return self.is_upper() and self.is_lower()
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def is_identity(self):
		if self.shape[0] == self.shape[1]:
			if self.is_diagonal():
				for i in range(self.shape[0]):
					if self[i][i] != 1:
						return False
					return True
			return False
		raise ValueError(f"The shape {self.shape} is not a shape of square matrix")

	def is_vertical(self):
		return self.shape[0] > self.shape[1]

	def is_horizontal(self):
		return self.shape[0] < self.shape[1]

	def is_scalar(self):
		if self.is_diagonal():
			return self.trace()/3 == self[0][0]
		return False

	def __repr__(self):
		# r = ''
		# for i in range(self.shape[0]):
		# 	for j in range(self.shape[1]):
		# 		r += str(self.matrix[i][j]) + '\t'
		# 	r += '\n'
		# return r
		return str(self.matrix)
