from re import M
import numpy as np 
import matplotlib.pyplot as plt 
import matrixOutils as MO           # Header to help us with some matrix manipulation
from scipy.signal import fftconvolve 
from PIL import Image as Img 


N = 480         # Pixels Uo 
zi = -50        # Distance of image [mm] 
zo = 75         # Distance to object [mm]
f = 50          # Focal length [mm] 

dx = 10e-3      # [mm] 
dy = 10e-3

lamb = 632.8e-6    # Wavelenght of Ne [mm]


def calculateC(zi, zo, lamb):
    return 1 / (lamb**2 * zi * zo)



def createW(As, dz, center):
    """ Returns the W function of the exponential term of the pupil """
    Ad = (dz / (2 * f**2))
    M = abs(zi / zo)

    def W(i, j):
        x = (i - center) * dx * M 
        y = (j - center) * dy * M 
        return As * (x**2 + y**2)**2 + Ad * (x**2 + y**2) 
        

    return W


def createPupil(pSize, As, dz, size = N):
    """ Creates a mask which will represent the pupil over the lens """ 

    y, x = np.ogrid[:size, :size]
    center = size // 2 

    pupil = (x - center)**2 + (y - center)**2 <= pSize**2 

    mask = np.zeros((size, size))

    mask[pupil] = 1
    
    Wfun = createW(As, dz, center) 
    
    W = np.fromfunction(Wfun, (size, size), dtype=float)
    

    return mask * np.exp(1j * 2 * np.pi / lamb * W) 


def createLens(diameter, As = 0, dz = 0):
    """ Given the diameter in mu m of the lens, creates the lens xD """ 
    return createPupil( diameter / 20, As, dz)


def createUg(objIm, M):
    """ Creates de Gaussian Geometric Amplitude of the image """ 

    newSize =abs( N // M ) 

    UoCropped = MO.cropMatrix(objIm, newSize)

    return (1 / M**2) * UoCropped



def createIg(objIm, C):
    """ Creates the I_i image (in frequency space) of objIm """ 
    
    M = abs(zi / zo) 

    Ug = createUg(objIm, M)

    return C**2 * (Ug * Ug.conj())


def createImage(objIm, P):
    """ Function that takes an object image and a mask in the real space 
    and returns the image image in real space """

    C = calculateC(zi, zo, lamb)

    PSF = np.abs(np.fft.fftshift(np.fft.fft2( P )))**2 
    Ig = createIg(objIm, C) 


    return np.abs(fftconvolve(Ig, PSF, mode = "same"))




fig, axes = plt.subplots(nrows = 6, ncols = 9, figsize = (14, 8.5))

for a in range(6):
    for _dz in range(9):

        # The pupil has to be from 100 to 400 pixels wide
        pupil = createLens(6000, As = a*10 / (2 * f**2), dz = -10 + _dz * 2.5)

        img = np.array(Img.open("img.TIF")) 
        resultingImage = createImage(img, pupil)

        ax = axes[a, _dz]
        ax.imshow(MO.cropMatrix(resultingImage, 480), cmap = "viridis")

        if a == 5: 
            ax.set_xlabel(rf"$\Delta z = {-10 + _dz * 2.5}$", fontsize = 14)
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        if _dz == 0:
            ax.set_ylabel(rf"$a_s = {a*2}$", fontsize = 14)
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        
        if a != 5 and _dz != 0: 
            ax.set_axis_off()


# Add global labels
# fig.text(0.5, 0.04, r'$\Delta z$ [mm]', ha='center', fontsize=30)
# fig.text(0.04, 0.5, r'$a_s', va='center', rotation='vertical', fontsize=30)
# plt.savefig("6mm paper.png", bbox_inches = 'tight', pad_inches = 0)
plt.show()


# The pupil has to be from 100 to 400 pixels wide
# pupil = createLens(4000, As = 0, dz = -10)
#
#
# img = np.array(Img.open("img.TIF")) 
# resultingImage = createImage(img, pupil)
#
# plt.imshow(resultingImage, cmap = "viridis")
# plt.axis("off")
# plt.savefig("d-10.png")
