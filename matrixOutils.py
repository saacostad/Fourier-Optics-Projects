import numpy as np 


def cropMatrix(matrix, M):
    """ Crops an NxN matrix into a new MxM matrix """ 
    N = matrix.shape[0]

    # If same size → nothing to do
    if M == N:
        return matrix.copy()

    elif M < N:
        # Center crop
        start = int((N - M) // 2)
        end = int(start + M)
    
        return matrix[start:end, start:end]

    else:
        # Center pad
        pad_total = int(M - N)
        pad_before = pad_total // 2
        pad_after = pad_total - pad_before
        return np.pad(matrix, ((pad_before, pad_after), (pad_before, pad_after)), mode='constant')

