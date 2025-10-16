import numpy as np 
import matplotlib.pyplot as plt 
import matrixOutils as MO           # Header to help us with some matrix manipulation
from scipy.signal import fftconvolve 
from PIL import Image as Img 


N = 480

def createPupil(pSize, size = N):
    """ Creates a mask which will represent the pupil over the lens """ 

    y, x = np.ogrid[:size, :size]
    center = size // 2 

    pupil = (x - center)**2 + (y - center)**2 <= pSize**2 

    mask = np.zeros((size, size))

    mask[pupil] = 1

    return mask 



def createUo(objIm, phase):
    """ Creates the complex amplitude distribution """
    return np.sqrt(objIm) * np.exp( 1j * phase )
    # This in case we had no information about Yobanni 



def createUg(objIm, M, phase):
    """ Creates de Gaussian Geometric Amplitude of the image """ 

    newSize =abs( N // M ) 

    UoCropped = MO.cropMatrix(createUo(objIm, phase), newSize)

    return (1 / M**2) * UoCropped



def createIg(objIm, C):
    """ Creates the I_i image (in frequency space) of objIm """ 
    
    phase = np.ones( (N, N) )
    M = 1.4                     # TODO check what's the actual magnification factor

    Ug = createUg(objIm, M, phase)

    return C**2 * (Ug * Ug.conj())


def createImage(objIm, h):
    """ Function that takes an object image and a mask in the real space 
    and returns the image image in real space """

    C = 0.02

    PSF = np.abs(np.fft.fftshift(np.fft.fft2( h )))**2 
    Ig = createIg(objIm, C) 

    return np.abs(fftconvolve(Ig, PSF))


pupil = createPupil(20)
img = np.array(Img.open("img.TIF")) 



resultingImage = createImage(img, pupil)

plt.imshow(resultingImage)
plt.savefig("img.png")
