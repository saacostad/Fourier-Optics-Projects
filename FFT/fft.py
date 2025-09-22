from logging import raiseExceptions
import numpy as np 
import matplotlib.pyplot as plt 
import cv2 as cv
from scipy.signal import fftconvolve, convolve2d





samples = 10
mask = "NONE"
mask_size = 1.0
width = 1.0

#------------------------------------------
#       FUNCIONES PARA EL PRIMER PUNTO
#------------------------------------------

def fixNonSquareImage(image):
    """ Checks if the image is squared, else, squares it """
    sizeX, sizeY = image.shape
    
    newSize = min([sizeX, sizeY]) + min([sizeX, sizeY])%2 - 1  

    if sizeX != sizeY:
        return image[:newSize, :newSize]
    else:
        return image 


def createSample(image, sample = samples):
    """ Samples the image each <sample> pixels """

    size, sizeY = image.shape

    pixel_jump = int(size / sample)
    
    sampled_image = np.zeros((size, sizeY), dtype = int)

    for i in range(pixel_jump):
        for j in range(pixel_jump):

            sampled_image[i * sample][j * sample] = image[i * sample][j * sample]


    return sampled_image


def makeFourierTransform(image):
    """ Makes the Fourier Transform of the image """ 

    F = np.fft.fft2(image)             
    Fshift = np.fft.fftshift(F)     

    return Fshift


def createFFTMask(image, sample = samples, type = "NONE", MaskSize = 1):
    """ returns a binary matrix where the 1s are the pixels in the spectrum that will be left """
   
    imageSize, trash = image.shape

    center = int(imageSize / 2)
    global width

    width = int(imageSize / (2 * sample))

    matrix = np.zeros((imageSize, imageSize))
    
    width = int(MaskSize * width)
 
    # Squared mask
    if type == "SQUARE" or type == "s":
        for i in range(center - width, center + width):
            for j in range(center - width, center + width):
                matrix[i, j] = 1.0
    
    # Round mask
    elif type == "CIRCLE" or type == "c":
        for i in range(center - width, center + width):
            for j in range(center - width, center + width):

                if np.sqrt( (center - i)**2 + (center - j)**2 ) < width:
                    matrix[i, j] = 1.0
    elif type == "HANN":
       # window1d = np.array([np.pow(np.sin( np.pi * i / (imageSize) ), 2) for i in range(0, imageSize)])
       
       window1d = np.zeros(imageSize)

       for i in range(center - width, center + width):
           window1d[i] = np.pow(np.sin( np.pi * (i - center + width) / (2 * width) ), 2)
       
       matrix = window1d[:, np.newaxis] * window1d[np.newaxis, :]
    elif type == "NONE":
        matrix = np.ones((imageSize, imageSize))
    else:
        return 0

    return matrix 




def filterFFT(FFTimage, mask):
    """ Given a mask, operates the FFTimage with it """

    return FFTimage * mask 
            


def makeInverseTransform(image):
    """ Makes the Inverse Fourier Transform """
    return np.fft.ifft2(np.fft.ifftshift(image))


# ---------------------------------------------
#       FUNCIONES PARA EL SEGUNDO PUNTO
# ---------------------------------------------

def createConvMask(fftMask, MaskSize = 1.0):
    
    convMask = np.abs(np.fft.fftshift(np.fft.ifft2(fftMask)))
    nwidth = int(MaskSize * width) 
    imageSize, trash = fftMask.shape
    center = int(imageSize / 2)

    matrix = np.zeros((2*nwidth + 1, 2*nwidth + 1))

    for i in range(2*nwidth + 1):
        for j in range(2*nwidth + 1):
            matrix[i, j] = convMask[center - nwidth + i, center - nwidth + j]
    

    return matrix

def reconstructFromConvolution(sImg, mask, MaskSize = 1.0):
    """ Reconstruct the image from the convolution """
    convMask = createConvMask(mask, MaskSize)

    return fftconvolve(sImg, convMask, mode = "same")
