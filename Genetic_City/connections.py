import numpy as np

def include_roads(matrix):
    newMatrix = np.zeros((matrix.shape[0]*2-1, matrix.shape[1]*2-1)) #Place holder
    for i in np.arange(newMatrix.shape[0]):
        for j in np.arange(newMatrix.shape[1]):
            if i%2==0:
                if j%2==0:
                    newMatrix[i,j]=matrix[int(i/2),int(j/2)]
                else:
                    newMatrix[i,j] = matrix[int(i/2),int((j-1)/2)] if matrix[int(i/2),int((j-1)/2)]==matrix[int(i/2),int((j+1)/2)] else 4
            else:
                if j%2==0:
                    newMatrix[i,j] = matrix[int((i-1)/2),int(j/2)] if matrix[int((i-1)/2),int(j/2)]==matrix[int((i+1)/2),int(j/2)] else 4
    for i in np.arange(1,newMatrix.shape[0],2):
        for j in np.arange(1,newMatrix.shape[1],2):
            newMatrix[i,j] = max(newMatrix[i,j-1],newMatrix[i,j+1],newMatrix[i-1,j],newMatrix[i+1,j])
    return newMatrix

#TODO: this matrix is not finished
def matrix_for_visualization(matrix):
    newMatrix = np.zeros((np.shape(matrix)[0]*2-np.shape(matrix)[0]//2, np.shape(matrix)[1]*2-np.shape(matrix)[1]//2)) #Place holder
    for i in np.arange(np.shape(matrix)[0]):
        for j in np.arange(np.shape(matrix)[1]):
            if i%2==0:
                source_i = int(i*3/2)
                if j%2==0:
                    source_j = int(j*3/2)
                    newMatrix[source_i,source_j]=matrix[int(i),int(j)]
                    newMatrix[source_i+1,source_j]=matrix[int(i),int(j)]
                    newMatrix[source_i,source_j+1]=matrix[int(i),int(j)]
                    newMatrix[source_i+1,source_j+1]=matrix[int(i),int(j)]
                else:
                    source_j = int(j*2-j//2)
                    newMatrix[source_i,source_j] = matrix[int(i),int(j)]
                    newMatrix[source_i+1,source_j] = matrix[int(i),int(j)]
            else:
                source_i = int(i*2-i//2)
                if j%2==0:
                    source_j = int(j*3/2)
                    newMatrix[source_i,source_j] = matrix[int(i),int(j)]
                    newMatrix[source_i,source_j+1] = matrix[int(i),int(j)]
                else:
                    source_j = int(j*2-j//2)
                    newMatrix[source_i,source_j] = matrix[int(i),int(j)]
    return newMatrix
'''test_matrix = np.asarray([[1,1,2],[1,1,2],[3,3,3]])
print("Original Matrix: ")
print(test_matrix)
matrix_w_roads = include_roads(test_matrix)
print("Matrix with roads: ")
print(matrix_w_roads)
print("Matrix with roads amplified: ")
print(matrix_for_visualization(matrix_w_roads))'''