import customtkinter as ctk 
import Fresnel as F 
import __main__ as G
from PIL import Image
from tkinter import filedialog 
import numpy as np 



""" ---------------------------------
    BUTTONS FOR DIFFRACTION IMAGE """


def update_distance_slider(value):
    F.distance = value
    G.distanceSliderLabel.configure(text = f"Distance: {int(value)} [mu m]")
    updateGeneral()


""" -------------------------------
    BUTTONS FOR MASK MENU       """

def update_size_slider(value):
    F.size = value 
    G.sizeSliderLabel.configure(text = f"Size: {int(value)}")
    updateGeneral()

def update_xpos_slider(value):
    F.xpos = value 
    G.xposSliderLabel.configure(text = f"Position in x: {int(value)}")
    updateGeneral()

def update_ypos_slider(value):
    F.ypos = value 
    G.yposSliderLabel.configure(text = f"Position in y: {int(value)}")
    updateGeneral()


def updateGeneral(opt = None):
    shape = G.maskOptionsBox.get()
    size = int(G.sizeSlider.get())
    xpos = int(G.xposSlider.get())
    ypos = int(G.yposSlider.get())
    
    size1 = None 
    size2 = None 

    if shape == "rectangle":
       
        if G.arg1Entry.get() == "":
            size1 = 4*size 
        else:
            size1 = int(int(G.arg2Entry.get()) * size / 10)

        if G.arg2Entry.get() == "":
            size2 = size 
        else: 
            size2 = int(int(G.arg1Entry.get()) * size / 10)
 

    tempMask = F.mask.copy()
    

    if G.doMesh.get():

        if G.repsEntry.get() == "":
            reps = 3 
        else:
            reps = int(G.repsEntry.get())

        if G.sepEntry.get() == "":
            seps = 100 
        else: 
            seps = int(G.sepEntry.get())

        F.createGrid(tempMask, shape, int(size * 10 / F.dx), int(reps), seps, xpos, ypos, size1, size2, not G.horCheck.get())
    else:
        F.modifyTempMask(tempMask, shape, int(size * 10 / F.dx), (xpos, ypos), kargs=[size1, size2])


    G.mask_image_holder.configure(image = G.convertImage(tempMask, G.maskWidth), text = "")

    dif_image = F.ft_Fresnel(tempMask, F.distance)

    Amin, Amax = dif_image.min(), dif_image.max()
    dif_scaled = (dif_image - Amin) / (Amax - Amin) * 255

    G.diffImageHolder.configure(image = G.convertImage(dif_scaled, G.difWidth))


def applyChanges():
    shape = G.maskOptionsBox.get()
    size = int(G.sizeSlider.get())
    xpos = int(G.xposSlider.get())
    ypos = int(G.yposSlider.get())


    size1 = None 
    size2 = None 

    if shape == "rectangle":
       
        if G.arg1Entry.get() == "":
            size1 = 4*size 
        else:
            size1 = int(int(G.arg2Entry.get()) * size / 10)

        if G.arg2Entry.get() == "":
            size2 = size 
        else: 
            size2 = int(int(G.arg1Entry.get()) * size / 10)


    if G.doMesh.get():

        if G.repsEntry.get() == "":
            reps = 3 
        else:
            reps = int(G.repsEntry.get())

        if G.sepEntry.get() == "":
            seps = 100 
        else: 
            seps = int(G.sepEntry.get())

        F.createGrid(F.mask, shape, size, int(reps), seps, xpos, ypos, size1, size2, not G.horCheck.get())
    else:
        F.modifyMask(F.mask, shape, size, (xpos, ypos), mode = 1, kargs=[size1, size2])


    G.mask_image_holder.configure(image = G.convertImage(F.mask, G.maskWidth), text = "")





def restartMask():
    F.mask[::, ::] = np.zeros((F.width, F.width))
    updateGeneral()

def saveImage():
    im_to_save = Image.fromarray((F.mask * 255).astype(np.uint8))

    filepath = filedialog.asksaveasfilename(
                defaultextension=".png"
            )

    if filepath:
        im_to_save.save(filepath)


def loadImage():
    filepath = filedialog.askopenfilename()

    if filepath:
        F.mask[::, ::] = np.array(Image.open(filepath)) / 255 

    G.mask_image_holder.configure(image = G.convertImage(F.mask, G.maskWidth), text = "")
