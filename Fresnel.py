import numpy as np 
import matplotlib.pyplot as plt 




width = 481
center = (width // 2) + 1
lamb = 633e-6                   # Wavelenght He-Ne given in [mm]

mask = np.zeros((width, width), dtype = bool)



size = 10

xpos = 0
ypos = 0

distance = 1000



def modifyMask(matrix, shape, size = 10, position = (0, 0), kargs = None):
    """ Taking an already existing mask, it modifies it by creating a hole according to the given paramenters """    
    match shape:
        case "square":

           matrix[(center-position[0]) - size:(center-position[0]) + size, (center-position[1]) - size:(center-position[1]) + size] = 1

        case "circle":

            Y, X = np.ogrid[:width, :width]
            prov = (X - (center + position[0]))**2 + (Y - (center + position[1]))**2 <= size**2

            matrix[::, ::] = np.logical_or(matrix, prov)

        case "rectangle":

           sizex, sizey = kargs[0], kargs[1]
           matrix[(center-position[0]) - sizex:(center-position[0]) + sizex, (center-position[1]) - sizey:(center-position[1]) + sizey] = 1




def ft_Fresnel(mask, d):
    """ Applies the Fourier Transform needed to see the difraction pattern """    
    eulerMask = np.fromfunction(lambda x, y: np.exp(1j * np.pi / (d * lamb) * ( (x - center)**2 + (y - center)**2)), (width, width))
    
    plt.imshow(np.real(eulerMask))
    plt.show()

    tempFT = np.fft.fft2( mask * eulerMask )

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
               

                

