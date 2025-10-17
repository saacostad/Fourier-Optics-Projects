import numpy as np 


def cropMatrix(matrix, Pg):
    """ Crops an NxN matrix into a new MxM matrix """ 
    N = matrix.shape[0]

    # If same size → nothing to do
    if N == Pg:
        return matrix.copy()

    elif Pg < N:
        # Center crop
        start = int((N - Pg) // 2)
        end = int(start + Pg)
    
        return matrix[start:end, start:end]

    else:
        # Center pad
        pad_total = int(Pg - N)
        pad_before = pad_total // 2
        pad_after = pad_total - pad_before
        return np.pad(matrix, ((pad_before, pad_after), (pad_before, pad_after)), mode='constant')

