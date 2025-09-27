import customtkinter as ctk 
import matplotlib.pyplot as plt 
from PIL import Image, ImageTk 


import Fresnel as F     # Python script where there are all the Fresnel functions needed
import guiButtons as B     # Python script with the functions that each button do 


""" -------------------------------
        IMPORTANT CONSTANTS     """

maskWidth = 450
difWidth = 450


""" -------------------------------
        HANDY FUNCTIONS         """

def convertImage(img, shape):
    """ Takes a numpy matrix and returns a displayable object """
    return ImageTk.PhotoImage( ((Image.fromarray(img)).convert("RGB")).resize((shape, shape), Image.NEAREST) )

""" -------------------------------
        APP DEFINITION          """

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Fresnel difraction")
app.geometry("1280x720")


# Set the geometry of the GUI 
app.grid_columnconfigure(0, weight = 2)     # The maskMenu will be twice as big as the difraction image 
app.grid_columnconfigure(1, weight = 1)


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
maskOptionsBox = ctk.CTkOptionMenu(generalMenu, values = ["square", "circle", "rectangle"])
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



""" Mask Image Holder Manu """

mask_image_holder = ctk.CTkLabel(maskImageMenu, width = maskWidth, height = maskWidth, image = convertImage(F.mask, maskWidth), text = "")
mask_image_holder.grid(row = 0, column = 0)

applyButton = ctk.CTkButton(maskImageMenu, text = "APPLY")
applyButton.grid(row = 1, column = 0, pady = 10)

selectMaskButton = ctk.CTkButton(maskImageMenu, text = "open mask")
selectMaskButton.grid(row = 2, column = 0)


""" ---------------------------
        DIFFRACTION MENU    """

# We create a frame for the diffraction image  
difMenu = ctk.CTkFrame(app)
# difMenu.grid(column = 1, row = 0, padx = 0, pady = 0, sticky = "")
difMenu.pack(side="left", expand = True)

diffImageHolder = ctk.CTkLabel(difMenu, width = difWidth, height = difWidth, image = convertImage(F.mask, difWidth), text = "")
diffImageHolder.grid(row = 0, column = 0, sticky = "nsew", padx = 0, pady = 0)


distanceSliderLabel = ctk.CTkLabel(difMenu, text = f"Distance: {F.distance} [mm]")
distanceSliderLabel.grid(row = 1, column = 0)

distanceSlider = ctk.CTkSlider(master = difMenu,
                               from_ = 100, to = 5000,
                               number_of_steps = 49,
                               command = B.update_distance_slider)
distanceSlider.set(1000)
distanceSlider.grid(row = 2, column = 0)


app.mainloop()
