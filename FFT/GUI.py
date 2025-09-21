from cv2 import samples
import fft
import customtkinter as ctk 
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np 
import matplotlib.pyplot as plt

#------------------------------------------------
#       BUTTON'S FUNCTIONS 
#------------------------------------------------

# Function to select and show image
def open_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*")]
    )
    if file_path:
        # Open image with PIL
        fft.img = Image.open(file_path).convert("L")
        fft.img = fft.img.resize((renderImage, renderImage))  # Resize for display
        tk_img = ImageTk.PhotoImage(fft.img)

        # Update label
        image_label.configure(image=tk_img, text="")
        image_label.image = tk_img  # keep reference!


def updateAll():
    """ Once we click the analyse button, it performs all the analisys for us """

    # Check the sample entry, it shall be an integer number
    try:
        fft.samples = int(sample_entry.get())
    except:
        # Default sample is 5
        fft.samples = 5
 
    orImgMax = np.array(fft.img).max()

    # We create the sampled image
    npSampled_IMAGE = fft.createSample(np.array(np.array(fft.img, dtype = float)), fft.samples)
    sampled_IMAGE = Image.fromarray(npSampled_IMAGE.astype(np.uint8))

    # Render the sampled image
    TKSampled_image = ImageTk.PhotoImage(sampled_IMAGE)

    sampled_img_label.configure(image=TKSampled_image, text="")
    sampled_img_label.image = TKSampled_image


    # We perform the Fourier Transform of the sampled image
    npFFT = fft.makeFourierTransform(npSampled_IMAGE)
    npFFT_image = np.log(np.abs(npFFT))


    """ Create the mask for the spectra """
    # Change the mask size 
    try:
        fft.mask_size = float(entry_mask_size.get())
    except:
        # Default sample is 5
        fft.mask_size = 1.0

    specMask = fft.createFFTMask(npFFT, sample=fft.samples, type = fft.mask, MaskSize=fft.mask_size)

    """ Render the spectra + the mask """
    # We normalize the spectra to be displayed in the app
    npFFT_image = npFFT_image * specMask
    npFFT_image = npFFT_image - npFFT_image.min()           
    npFFT_image = npFFT_image / npFFT_image.max()  
    npFFT_image = (npFFT_image * 255).astype(np.uint8)


    # Render the spectra
    TKSpectrum_image = ImageTk.PhotoImage(Image.fromarray(npFFT_image))

    FFTSPEC_img_label.configure(image=TKSpectrum_image, text="")
    FFTSPEC_img_label.image = TKSpectrum_image



    """ Recover the image """
    npRecFFT = np.abs(fft.makeInverseTransform(npFFT * specMask))
    
    npRecFFT = npRecFFT / npRecFFT.max()  
    npRecFFT = (npRecFFT * 255).astype(np.uint8)

    TK_FFT_RECO_image = ImageTk.PhotoImage(Image.fromarray(npRecFFT))

    FFT_recovered_img_label.configure(image=TK_FFT_RECO_image, text="")
    FFT_recovered_img_label.image = TKSpectrum_image


    """ Show the convolution mask """
    try:
        fft.conv_mask_size = float(entry_conv_mask_size.get())
    except:
        # Default sample is 5
        fft.conv_mask_size = 1.0

    convMask = (fft.createConvMask(specMask, MaskSize=fft.conv_mask_size))

    convMask = convMask / convMask.max()  
    convMask = (convMask * 255).astype(np.uint8)

    TK_CONV_mask_image = ImageTk.PhotoImage(Image.fromarray(convMask).resize((renderImage, renderImage)))

    CONV_MASK_img_label.configure(image=TK_CONV_mask_image, text="")
    CONV_MASK_img_label.image = TK_CONV_mask_image


    """ Show the recovered image from convolution """

    rec_conv_img = fft.reconstructFromConvolution(npSampled_IMAGE, convMask, MaskSize=fft.conv_mask_size)

    rec_conv_img = rec_conv_img / rec_conv_img.max()  
    rec_conv_img = (rec_conv_img * 255).astype(np.uint8)

    TK_CONV_rec_image = ImageTk.PhotoImage(Image.fromarray(rec_conv_img).resize((renderImage, renderImage)))

    CONV_rec_img_label.configure(image=TK_CONV_rec_image, text="")
    CONV_rec_img_label.image = TK_CONV_rec_image


def mask_menu_update(choice):
    fft.mask = choice
    updateAll()

#------------------------------------------------
#       CREATION OF THE GUI 
#------------------------------------------------

""" We create the GUI application """

firstImageRow = 2 
secondImageRow = 6

selectionButtonsRow = 0 
firstImageTitleRow = 1 

entryRow = 3 
entrySlidersRow = 4 
secondImageTitleRow = 5 

analyseRow = 7

renderImage = 351

ctk.set_appearance_mode("Dark") 
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("FFT")
app.geometry("1800x1000")

imgF = ctk.CTkFrame(app)
imgF.pack(pady=0, padx=0, fill="both", expand=True)

""" We set a grid for aesthetics """

for r in range(5):
    imgF.grid_rowconfigure(r, weight=1)
for c in range(3):
    imgF.grid_columnconfigure(c, weight=1)


""" Label and button to open the image """
# Placeholder for the image
image_label = ctk.CTkLabel(imgF, text="NO IMAGE LOADED", width=renderImage, height=renderImage, fg_color="black")
image_label.grid(row = firstImageRow, column = 0, padx = 0, pady = 0, sticky = "")

# Button to select image
open_button = ctk.CTkButton(imgF, text="OPEN", command=open_image)
open_button.grid(row=selectionButtonsRow, column=0, padx=0, pady=0, sticky="")

# Title of the image 
image_title = ctk.CTkLabel(imgF, text = "ORIGINAL IMAGE", corner_radius=0)
image_title.grid(row=firstImageTitleRow, column = 0, sticky="s")

""" Label and button to sample the image """
# Placeholder for the sampled image
sampled_img_label = ctk.CTkLabel(imgF, text="NO SAMPLED IMAGE", width=renderImage, height=renderImage, fg_color="black")
sampled_img_label.grid(row = secondImageRow, column = 0, padx = 0, pady = 0, sticky = "")

# Entry for the sampling spacing
# sample_entry = ctk.CTkEntry(imgF, placeholder_text="SAMPLING SPACING")
# sample_entry.grid(row = 2, column = 0, padx = 0, pady = 0, sticky = "")
sample_text = ctk.CTkLabel(imgF, text = "Sampling spacing:   5")
sample_text.grid(row = entryRow, column = 0)


def updateSampleLabel(sample):
    sample_text.configure(text=f"Sampling spacing:   {int(sample)}")
    updateAll()

sample_entry = ctk.CTkSlider(master = imgF, 
                             from_ = 1,
                             to = 20,
                             number_of_steps=19,
                             command=updateSampleLabel)
sample_entry.grid(row = entrySlidersRow, column = 0, padx = 0, pady = 0, sticky="n")
sample_entry.set(5)



# Button to sample the thing
sample_button = ctk.CTkButton(imgF, text="ANALYSE", command=updateAll,
                              fg_color = "orange",
                              height = 60,
                              text_color = "black")
sample_button.grid(row=selectionButtonsRow, column=2, padx=0, pady=0, sticky="")


""" Label for the sampled image spectrum """
# Placeholder for the FFT spectrum image

S_image_title = ctk.CTkLabel(imgF, text = "SAMPLED IMAGE", corner_radius=0)
S_image_title.grid(row=secondImageTitleRow, column = 0)

FFTSPEC_img_label = ctk.CTkLabel(imgF, text="NO SPECTRUM IMAGE", width=renderImage, height=renderImage, fg_color="black")
FFTSPEC_img_label.grid(row = firstImageRow, column = 1, padx = 0, pady = 0, sticky = "")


""" Menu for mask selection in the spectra """
mask_options = ["none", "square", "circle", "Hann"]
mask_menu = ctk.CTkOptionMenu(imgF, values=mask_options, command=mask_menu_update)
mask_menu.grid(row = selectionButtonsRow, column = 1)

M_image_title = ctk.CTkLabel(imgF, text = "FREQUENCY DOMAIN", corner_radius=0)
M_image_title.grid(row=firstImageTitleRow, column = 1, sticky = "s")



# Entry to select the size of the mask
# entry_mask_size = ctk.CTkEntry(imgF, placeholder_text="FREQ MASK SIZE")
# entry_mask_size.grid(row = entrySlidersRow, column = 1, padx = 0, pady = 0, sticky = "")
maskSize_text = ctk.CTkLabel(imgF, text = "Freq. mask size:   1.0")
maskSize_text.grid(row = entryRow, column = 1)
def updateMaskSizeLabel(sample):
    maskSize_text.configure(text=f"Freq. mask size:   {round(sample, 1)}")
    updateAll()
entry_mask_size = ctk.CTkSlider(master = imgF, 
                             from_ = 0.1,
                             to = 5.0,
                             number_of_steps=49,
                             command=updateMaskSizeLabel)
entry_mask_size.grid(row = entrySlidersRow, column = 1, padx = 0, pady = 0, sticky="n")
entry_mask_size.set(1.0)

""" Placeholder for the recovered FFT image """
FFT_recovered_img_label = ctk.CTkLabel(imgF, text="NO RECOVERED IMAGE", width=renderImage, height=renderImage, fg_color="black")
FFT_recovered_img_label.grid(row = firstImageRow, column = 2, padx = 0, pady = 0, sticky = "")

FR_image_title = ctk.CTkLabel(imgF, text = "FFT RECOVERED IMAGE", corner_radius=0)
FR_image_title.grid(row=firstImageTitleRow, column = 2)

""" Placeholder for the convolution mask """
CONV_MASK_img_label = ctk.CTkLabel(imgF, text="NO CONV MASK IMAGE", width=renderImage, height=renderImage, fg_color="black")     
CONV_MASK_img_label.grid(row = secondImageRow, column = 1, padx = 0, pady = 0, sticky = "")

CM_image_title = ctk.CTkLabel(imgF, text = "CONV. MASK", corner_radius=0)
CM_image_title.grid(row=secondImageTitleRow, column = 1)

""" Placeholder for convoluted recovered image """

CR_image_title = ctk.CTkLabel(imgF, text = "CONV. RECOVERED IMAGE", corner_radius=0)
CR_image_title.grid(row=secondImageTitleRow, column = 2)

CONV_rec_img_label = ctk.CTkLabel(imgF, text="NO CONV REC IMAGE", width=renderImage, height=renderImage, fg_color="black")
CONV_rec_img_label.grid(row = secondImageRow, column = 2, padx = 0, pady = 0, sticky = "")


""" Entry for conv mask size """
# entry_conv_mask_size = ctk.CTkEntry(imgF, placeholder_text="CONV MASK SIZE")
# entry_conv_mask_size.grid(row = entrySlidersRow, column = 2, padx = 0, pady = 0, sticky = "")

ConvmaskSize_text = ctk.CTkLabel(imgF, text = "Conv. mask size:   1.0")
ConvmaskSize_text.grid(row = entryRow, column = 2)
def updateConvMaskSizeLabel(sample):
    ConvmaskSize_text.configure(text=f"Conv. mask size:   {round(sample, 1)}")
    updateAll()
entry_conv_mask_size = ctk.CTkSlider(master = imgF, 
                             from_ = 0.1,
                             to = 2.5,
                             number_of_steps=24,
                             command=updateConvMaskSizeLabel)
entry_conv_mask_size.grid(row = entrySlidersRow, column = 2, padx = 0, pady = 0, sticky="n")
entry_conv_mask_size.set(1.0)
# Run app
app.mainloop()

