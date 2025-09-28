import numpy as np 
import matplotlib.pyplot as plt
from numpy.matrixlib import matrix 




width = 1081
center = (width // 2) + 1
lamb = 633e-6                   # Wavelenght He-Ne given in [mm]
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



def createGrid(matrix, shape, size, reps, separation, arg1 = None, args2 = None):
    """ Creates a grid of a given shape """
    return None 


    
    

    



def ft_Fresnel(mask, d):
    """ Applies the Fourier Transform needed to see the difraction pattern """    
    eulerMask = np.fromfunction(lambda x, y: np.exp(1j * np.pi / (d * lamb) * ( (x*dx - center*dx)**2 + (y*dy - center*dy)**2)), (width, width))
        
    tempFT = np.fft.fft2( (mask) * eulerMask )
    return np.abs(np.fft.fftshift(tempFT))**2





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
               

                

