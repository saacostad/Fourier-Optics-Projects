import customtkinter as ctk 
import matplotlib.pyplot as plt 
from PIL import Image, ImageTk 


import Fresnel as F     # Python script where there are all the Fresnel functions needed
import guiButtons as B     # Python script with the functions that each button do 




""" -------------------------------
        HANDY FUNCTIONS         """

def convertImage(img, shape):
    """ Takes a numpy matrix and returns a displayable object """
    return ImageTk.PhotoImage( ((Image.fromarray(img))).resize((shape, shape)) )



""" -------------------------------
        APP DEFINITION          """

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Fresnel difraction")
app.geometry("1280x720")


# Set the geometry of the GUI 
app.grid_columnconfigure(0, weight = 2)     # The maskMenu will be twice as big as the difraction image 
app.grid_columnconfigure(1, weight = 2)



""" -------------------------------
        IMPORTANT CONSTANTS     """

maskWidth = 450
difWidth = 450

doMesh = ctk.BooleanVar(value = False)  # Boolean to know if we want to create a mesh 
horCheck = ctk.BooleanVar(value = True) # Boolean to create the mesh vertically or horizontally



""" ---------------------------
        MASK MENU           """

# We create a frame for the mask menu 
maskMenu = ctk.CTkFrame(app)
# maskMenu.grid(column = 0, row = 0, padx = 0, pady = 0, sticky = "nsew")   # Is placed on the left size of the app 
maskMenu.pack(side = "left", expand = True)

# We create the 3 main frames inside this frame 
generalMenu = ctk.CTkFrame(maskMenu)
generalMenu.grid(column = 0, row = 0, sticky = "nsew")

advancedMenu = ctk.CTkFrame(maskMenu)
advancedMenu.grid(column = 0, row = 1, sticky = "nsew")

maskImageMenu = ctk.CTkFrame(maskMenu)
maskImageMenu.grid(column = 1, row = 0, rowspan = 2, sticky = "")


""" General Parameters Menu """

generalMenuTitle = ctk.CTkLabel(generalMenu, text = "GENERAL MASK MENU")
generalMenuTitle.pack(pady = 10)

# MASK TYPE OPTION BOX 
maskOptionsBox = ctk.CTkOptionMenu(generalMenu, values = ["square", "circle", "rectangle"], command = B.updateGeneral)
maskOptionsBox.pack(pady = 10)


# SIZE SLIDER 
sizeSliderLabel = ctk.CTkLabel(generalMenu, text = f"size: {F.size}") 
sizeSliderLabel.pack()

sizeSlider = ctk.CTkSlider(generalMenu, 
                           from_ = 1, to = 50,
                           number_of_steps = 49,
                           command = B.update_size_slider)
sizeSlider.set(10)
sizeSlider.pack()


# X POSITION SLIDER     
xposSliderLabel = ctk.CTkLabel(generalMenu, text = f"Position in x: {F.xpos}") 
xposSliderLabel.pack()

xposSlider = ctk.CTkSlider(generalMenu, 
                           from_ = -400, to = 400,
                           number_of_steps = 80,
                           command = B.update_xpos_slider)
xposSlider.set(0)
xposSlider.pack()


# Y POSITION SLIDER     
yposSliderLabel = ctk.CTkLabel(generalMenu, text = f"Position in y: {F.ypos}") 
yposSliderLabel.pack()

yposSlider = ctk.CTkSlider(generalMenu, 
                           from_ = -400, to = 400,
                           number_of_steps = 80,
                           command = B.update_ypos_slider)
yposSlider.set(0)
yposSlider.pack()




""" Advanced Parameters Menu """

advMenuTitle = ctk.CTkLabel(advancedMenu, text = "ADVANCED MASK MENU")
advMenuTitle.grid(row = 0, column = 0, columnspan = 2, pady = 15)


meshCheckBox = ctk.CTkCheckBox(advancedMenu, text = "Create mesh", variable = doMesh)
meshCheckBox.grid(column = 0, row = 1, padx = 15)

horverCheckBox = ctk.CTkCheckBox(advancedMenu, text = "Horizontal mesh", variable = horCheck)
horverCheckBox.grid(column = 1, row = 1, padx = 15)


repsEntry = ctk.CTkEntry(advancedMenu, placeholder_text = "# wholes")
repsEntry.grid(column = 0, row = 2, pady = 15, padx = 10)

sepEntry = ctk.CTkEntry(advancedMenu, placeholder_text = "separation")
sepEntry.grid(column = 1, row = 2, pady = 15, padx = 10)


arg1Entry = ctk.CTkEntry(advancedMenu, placeholder_text = "adv. args 1")
arg1Entry.grid(column = 0, row = 3, pady = 15, padx = 10)


arg2Entry = ctk.CTkEntry(advancedMenu, placeholder_text = "adv. args 2")
arg2Entry.grid(column = 1, row = 3, pady = 15, padx = 10)


restartMaskButton = ctk.CTkButton(advancedMenu, text = "restart mask", command = B.restartMask, width = 30, corner_radius=0, bg_color="red")
restartMaskButton.grid(column = 0, row = 4, columnspan = 2, pady = 25)


""" Mask Image Holder Manu """

mask_image_title = ctk.CTkLabel(maskImageMenu, text = "GENERATED MASK")
mask_image_title.grid(row = 0, column = 0, columnspan = 3, pady = 20)

mask_image_holder = ctk.CTkLabel(maskImageMenu, width = maskWidth, height = maskWidth, image = convertImage(F.mask, maskWidth), text = "")
mask_image_holder.grid(row = 1, column = 0, columnspan = 3)

applyButton = ctk.CTkButton(maskImageMenu, text = "APPLY", command = B.applyChanges, corner_radius=0, height = 45)
applyButton.grid(row = 2, column = 0, pady = 10)

selectMaskButton = ctk.CTkButton(maskImageMenu, text = "open mask", width = 80, command=B.loadImage)
selectMaskButton.grid(row = 2, column = 1, padx = 10, sticky = "e")

saveMaskButton = ctk.CTkButton(maskImageMenu, text = "save mask", width = 80, command = B.saveImage)
saveMaskButton.grid(row = 2, column = 2, sticky = "w")


""" ---------------------------
        DIFFRACTION MENU    """
# We create a frame for the diffraction image  
difMenu = ctk.CTkFrame(app)
# difMenu.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = "")
difMenu.pack(side="left", expand = True)


dif_image_title = ctk.CTkLabel(difMenu, text = "DIFRACTED SIGNAL")
dif_image_title.grid(row = 0, column = 0, pady = 20)


diffImageHolder = ctk.CTkLabel(difMenu, width = difWidth, height = difWidth, image = convertImage(F.mask, difWidth), text = "")
diffImageHolder.grid(row = 1, column = 0, sticky = "nsew", padx = 0, pady = 0)


distanceSliderLabel = ctk.CTkLabel(difMenu, text = f"Distance: {F.distance} [mu m]")
distanceSliderLabel.grid(row = 2, column = 0)

distanceSlider = ctk.CTkSlider(master = difMenu,
                               from_ = 50000, to = 500000,
                               number_of_steps = 100,
                               command = B.update_distance_slider)
distanceSlider.set(1000)
distanceSlider.grid(row = 3, column = 0)


app.mainloop()
