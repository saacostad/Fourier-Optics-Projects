import numpy as np 
import matplotlib.pyplot as plt 
import matrixOutils as MO           # Header to help us with some matrix manipulation

N = 512

def createPupil(pSize, size = N):
    """ Creates a mask which will represent the pupil over the lens """ 

    y, x = np.ogrid[:size, :size]
    center = size // 2 

    pupil = (x - center)**2 + (y - center)**2 <= radius**2 

    mask = np.zeros((size, size))

    mask[pupil] = 1

    return mask 



def createUo(objIm, phase):
    """ Creates the complex amplitude distribution """
    return np.sqrt(objIm) * np.exp( 1j * phase )


def createUg(objIm, M, phase):
    """ Creates de Gaussian Geometric Amplitude of the image """ 

    newSize = N // M 
    
    UoCropped = MO.cropMatrix(createUo(objIm, phase), newSize)

    return (1 / M**2) * UoCropped

def createIg(objIm, C):
    """ Creates the I_i image (in frequency space) of objIm """ 



def createImage(objIm, h):
    """ Function that takes an object image and a mask in the real space 
    and returns the image image in real space """

    PSF = np.abs(np.fft.fftshift(np.fft.fft2( h )))**2 


