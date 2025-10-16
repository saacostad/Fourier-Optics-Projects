import numpy as np 
import matplotlib.pyplot as plt
from numpy.matrixlib import matrix 




width = 1081
center = (width // 2) + 1
lamb = 633e-3                   # Wavelenght He-Ne given in [mu m]
dx = dy = 20000/width # [mu m]


mask = np.zeros((width, width), dtype = bool)
tempMask = np.zeros((width, width), dtype = int)


size = 10

xpos = 0
ypos = 0

distance = 1000

reps = 5

separation = 10 

args1 = 10 
args2 = 20


def modifyMask(matrix, shape, size = 10, position = (0, 0), kargs = None, mode = 1):
    """ Taking an already existing mask, it modifies it by creating a hole according to the given paramenters """    
    match shape:
        case "square":

           matrix[(center-position[0]) - size:(center-position[0]) + size, (center-position[1]) - size:(center-position[1]) + size] = mode

        case "circle":

            Y, X = np.ogrid[:width, :width]
            prov = (X - (center + position[0]))**2 + (Y - (center + position[1]))**2 <= size**2

            matrix[::, ::] = np.logical_or(matrix, prov) * mode 

        case "rectangle":

           sizex, sizey = kargs[0], kargs[1]
           matrix[(center-position[0]) - sizex:(center-position[0]) + sizex, (center-position[1]) - sizey:(center-position[1]) + sizey] = mode 



def modifyTempMask(tempMask, shape, size, position = (0, 0), kargs = None):
    modifyMask(tempMask, shape, size, position, kargs, mode = 1)



def createGrid(matrix, shape, size, reps, separation, position2, position1, arg1 = None, arg2 = None, hor = True,):
    """ Creates a grid of a given shape """
    
    reps *= 2

    for z in range(int(-(((reps-reps%2 - 4) / 2) + 1) * separation / 2), int((((reps-reps%2 - 4) / 2) + 1) * separation / 2) + 1, separation):
        

        if hor and position1 + z + width/2 < width and position1 + z + width/2 > 0:
            modifyTempMask(matrix, shape, size, position = ( position1 + z, position2 ), kargs=(arg1, arg2))
        elif not hor and position2 + z + width/2 < width and position2 + z + width/2 > 0:
            modifyTempMask(matrix, shape, size, position = ( position1, position2 + z), kargs=(arg1, arg2))



def ft_Fresnel(mask, d):
    """ Applies the Fourier Transform needed to see the difraction pattern """   
    d = float(d)
    # eulerMask = np.fromfunction(lambda x, y: np.exp(1j * np.pi / (d * lamb) * ( (x*dx - center*dx)**2 + (y*dy - center*dy)**2)), (width, width))
        
    maskTransform = np.fft.fftshift(np.fft.fft2( mask ))
    constant = 1/(lamb**2)
    propMask = np.fromfunction(lambda i, j:  np.exp( 1j * np.pi * 2 * (d) * np.sqrt(0j + 0 +  constant + ( (( 1 / dx )**2) * ( (i - center)**2 - (j - center)**2 ) ) ) ), (width, width) )

    tempFT = np.fft.ifft2( (maskTransform) * propMask )
    
    return np.abs(tempFT)**2





#
# modifyMask(mask, "circle", size = 5)
#
#
# difPattern = ft_Fresnel(mask, 1000)
#
# plt.imshow(difPattern)
# plt.show()
#
#                 
               

                

