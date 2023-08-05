class Matrix:
    """
    Generic matrix class for creating matrices and
    performing basic operations scalar:matrix or matrix:matrix
    basic operations.

    Attributes:
    dims (int) defines the dimensions of the matrix
    row (int) representing the number of rows in a matrix
    col (int) representing the number of columns in a matrix
    """
    
    def __init__(self, dims, fill):
        self.rows = dims[0]
        self.cols = dims[1]

        self.A = [[fill] * self.cols for i in range(self.rows)]


    def __str__(self):
        """
        Function that prints out the matrix in multiple dimensions
        """
        m = len(self.A) # Get the first dimension
        mtxStr = ''
        
        mtxStr += '------------- output -------------\n'
    
        for i in range(m):
            mtxStr += ('|' + ', '.join( map(lambda x:'{0:8.3f}'.format(x), self.A[i])) + '| \n')

        mtxStr += '----------------------------------'

        return mtxStr

    def __add__(self, other):
        
        """
        Function creates and performs addtion operations.
        The operation is performed on between 2 matrices or between a scaler
        object - a single value.

        Parameters
        ----------
        self: matrix
            the original matrix

        other: float or matrix
            the second object which can be a float or a matrix
        Returns
        -------
            matrix: which is a sum of the original matrix and the other object
        """

        #Create a new matrix
        C = Matrix( dims = (self.rows, self.cols), fill = 0)

        #Check if the other object is of type Matrix
        if isinstance (other, Matrix):
            #Add the corresponding element of 1 matrices to another
            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] + other.A[i][j]

        #If the other object is a scaler
        elif isinstance (other, (int, float)):
            #Add that constant to every element of A
            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] + other


        return C

    #Right addition can be done by calling left addition
    def __radd__(self, other):
        """
        Function performs right addition  by calling left addition

        Parameters
        ----------
        other : float or matrix
            the second object

        Returns
        -------
        matrix : a sum of the original matric and a scaler or a second matrix.
        """
        return self.__add__(other)

    def __mul__(self, other): #pointwise multiplication
        
        """
        Function performs  multiplication between
        a matrix and a scaler or matrix

        steps: - Create a matrix
               - identify the other object (float or matrix)
               - Scaler multiplication
               - Point-wise multiplication
               - matrix-matrix multiplication

        Parameters
        ----------
        other: float or matrix
            second object to peform multiplication with the original matrix

        Returns
        -------
        Result_matrix:
            Result matrix the same number of rows and columns as the original matrix
        """

        C = Matrix( dims = (self.rows, self.cols), fill = 0)
        if isinstance(other, Matrix):

            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] * other.A[i][j]

        #Scaler multiplication
        elif isinstance(other, (int, float)):

            for i in range(self.rows):
                for j in range(self.cols):
                    C.A[i][j] = self.A[i][j] * other

        return C 

    #Point-wise multiplication is also commutative
    def __rmul__(self, other):
        
        """Function performs point-wise multiplication
        This operation can be performed on matrices of the same dimensions

        Parameters
        ----------
        other: float or matrix
            second object to peform multiplication with the original matrix

        Returns
        -------
        Result_matrix:
            Result matrix the same number of rows and columns as the original matrix

        """

        return self.__mul__(other)


    def __matmul__(self, other): #matrix-matrix multiplication
        
        """Function performs  multiplication between 2 matrices
        This operation can be performed on matrices of different sizes

        Parameters
        ----------
        other:matrix
            second object to peform multiplication with the original matrix
        Returns
        -------
        Result_matrix:
            The result matrix has the number of rows of the first and the number of columns of the second matrix.
        """
            

        if isinstance(other, Matrix):
            C = Matrix( dims = (self.rows, self.cols), fill = 0)

            #Multiply the elements in the same row of the first matrix 
            #to the elements in the same col of the second matrix
            for i in range(self.rows):
                for j in range(self.cols):
                    acc = 0

                    for k in range(self.rows):
                        acc += self.A[i][k] * other.A[k][j]

                    C.A[i][j] = acc

        return C

    def __getitem__(self, key):
        
        """Function that identifies the element 
        in a given position in a matrix

        Parameters
        ----------
        key:
        row[i] = row position
        col[j] = col position

        Returns
        -------
        Element in positiob[i][j]
        """
        if isinstance(key, tuple):
     
            i = key[0]
            j = key[1]
            return self.A[i][j]


    def __setitem__(self, key, value):
        
        """Function that replaces the element 
        in a given position in a matrix

        Parameters
        ----------
        key:
        row[i] = row position
        col[j] = col position
        Value  = new element in position [i][j]
        Returns
        -------
        Matrix with a new element in position[i][j]
        """
        
        if isinstance(key, tuple):
            i = key[0]
            j = key[1]
            self.A[i][j] = value