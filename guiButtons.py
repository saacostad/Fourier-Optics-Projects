import customtkinter as ctk 
import Fresnel as F 
import __main__ as G

""" ---------------------------------
    BUTTONS FOR DIFFRACTION IMAGE """


def update_distance_slider(value):
    F.distance = value
    G.distanceSliderLabel.configure(text = f"Distance: {int(value)} [mm]")



""" -------------------------------
    BUTTONS FOR MASK MENU       """

def update_size_slider(value):
    F.size = value 
    G.sizeSliderLabel.configure(text = f"Size: {int(value)}")


def update_xpos_slider(value):
    F.xpos = value 
    G.xposSliderLabel.configure(text = f"Position in x: {int(value)}")


def update_ypos_slider(value):
    F.ypos = value 
    G.yposSliderLabel.configure(text = f"Position in y: {int(value)}")
