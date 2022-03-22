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