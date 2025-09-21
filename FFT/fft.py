from logging import raiseExceptions
import numpy as np 
import matplotlib.pyplot as plt 
import cv2 as cv
from scipy.signal import fftconvolve, convolve2d



img = cv.imread("images/3.jpg", cv.IMREAD_GRAYSCALE)
samples = 10
mask = "none"
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


def createFFTMask(image, sample = samples, type = "none", MaskSize = 1):
    """ returns a binary matrix where the 1s are the pixels in the spectrum that will be left """
   
    imageSize, trash = image.shape

    center = int(imageSize / 2)
    global width

    width = int(imageSize / (2 * sample))


    matrix = np.zeros((imageSize, imageSize))
    
    width = int(MaskSize * width)

    
    # Squared mask
    if type == "square" or type == "s":
        for i in range(center - width, center + width):
            for j in range(center - width, center + width):
                matrix[i, j] = 1.0
    
    # Round mask
    elif type == "circle" or type == "c":
        for i in range(center - width, center + width):
            for j in range(center - width, center + width):

                if np.sqrt( (center - i)**2 + (center - j)**2 ) < width:
                    matrix[i, j] = 1.0
    elif type == "Hann":
       # window1d = np.array([np.pow(np.sin( np.pi * i / (imageSize) ), 2) for i in range(0, imageSize)])
       
       window1d = np.zeros(imageSize)

       for i in range(center - width, center + width):
           window1d[i] = np.pow(np.sin( np.pi * (i - center + width) / (2 * width) ), 2)
       
       matrix = window1d[:, np.newaxis] * window1d[np.newaxis, :]
    elif type == "none":
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

    matrix = np.zeros((2*nwidth, 2*nwidth))

    for i in range(2*nwidth):
        for j in range(2*nwidth):
            matrix[i, j] = convMask[center - nwidth + i, center - nwidth + j]
    

    return matrix



def reconstructFromConvolution(sImg, mask, MaskSize = 1.0):
    """ Reconstruct the image from the convolution """
    # convMask = np.abs(np.fft.fftshift(np.fft.ifft2(mask)))
    #
    # convMask *= mask
    #
    # # Get bounding box of non-zeros
    # rows, cols = np.nonzero(convMask)
    # rmin, rmax = rows.min(), rows.max()
    # cmin, cmax = cols.min(), cols.max()
    #
    # # Crop
    # convMaskCropped = convMask[rmin:rmax+1, cmin:cmax+1]

    convMask = createConvMask(mask, MaskSize)

    return fftconvolve(sImg, convMask, mode = "same")

#
#
# squareImage = fixNonSquareImage(img)
# sampledImage = createSample(squareImage, sample=samples)
# FTImage = makeFourierTransform(sampledImage)
# mask = createFFTMask(FTImage, MaskSize = 1, type = "square")
#
#
# filteredFFT = filterFFT(FTImage, mask)
#
#
# recoveredImage = makeInverseTransform(filteredFFT)
#
# plt.imshow(sampledImage)
# plt.show()
#
#
# plt.imshow(np.abs(recoveredImage))
# plt.show()
#
#
# plt.imshow(mask)
# plt.show()
#
#
# convMask = np.abs(reconstructFromConvolution(sampledImage, mask, MaskSize=1.0))
#
# plt.imshow(convMask)
# plt.show()
