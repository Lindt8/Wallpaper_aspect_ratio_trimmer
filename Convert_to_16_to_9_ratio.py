'''
Created on Jun 19, 2016

@author: Hunter
'''
'''
The purpose of this package is to convert background images to a 16:9 aspect ratio.
It seeks to produce several different altered versions of the input image, and the user
can then save the one(s) that are desirable.

Cases for input image:
W/H > 16/9  (x dimension must be trimmed)
    - Trim from left
    - Trim from right
    - Trim from both edges to keep image centered
W/H < 16/9  ( y dimension must be trimmed
    - Trim from top
    - Trim from bottom
    - Trim from both edges to keep image centered
'''

import os
from tkinter import *
from tkinter import Tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageChops
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def close_window(): #Used in GUIs
    root.quit()
    root.destroy()

desired_WoH_ratio = 16/9

folder_not_16to9 = r"D:\Libraries\Pictures\Backgrounds\Not 16 to 9"
folder_is_16to9  = r"D:\Libraries\Pictures\Backgrounds\16 to 9"
newfile_suffix = "_16to9"

win1 = Tk()
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
path_img = filedialog.askopenfilename(initialdir=folder_not_16to9, title="Select image to be cropped") # show an "Open" dialog box and return the path to the selected file
win1.destroy()
base = os.path.basename(path_img)
filename, ext = os.path.splitext(base)
newfile_path_noex = folder_is_16to9 + "\\" + filename + newfile_suffix

im_org = Image.open(path_img)
im = im_org.copy()

use_trimmer = True
if use_trimmer: im = trim(im)

w, h = im.size

# Determine which dimension should be trimmed
if w/h <= 1.01*(desired_WoH_ratio) and w/h >= 0.99*(desired_WoH_ratio):
    print("Image is already 16:9.")
    sys.exit()
elif w/h > 1.01*(desired_WoH_ratio):
    print("Image is too wide; trim from left and/or right.")
    trim_side = 0
    new_w = int((desired_WoH_ratio)*h)
    dw = w - new_w
elif w/h < 0.99*(desired_WoH_ratio):
    print("Image is too tall; trim from top and/or bottom.")
    trim_side = 1
    new_h = int((1/desired_WoH_ratio)*w)
    dh = h - new_h

if trim_side == 0:
    # trim width (x) dimension
    ymin1, ymin2, ymin3 = h, h, h
    ymax1, ymax2, ymax3 = 0, 0, 0
    # Left trim
    xmin1 = dw
    xmax1 = w
    t1 = "Left"
    # Right trim
    xmin2 = 0
    xmax2 = w - dw
    t3 = "Right"
    # Centered trim
    xmin3 = int(0 + (dw/2))
    xmax3 = int(w - (dw/2))
    
elif trim_side == 1:
    # trim height (y) dimension
    xmin1, xmin2, xmin3 = 0, 0, 0
    xmax1, xmax2, xmax3 = w, w, w
    # Bottom trim
    ymax1 = 0
    ymin1 = h - dh
    t1 = "Bottom"
    # Top trim
    ymax2 = dh
    ymin2 = h
    t3 = "Top"
    # Centered trim
    ymax3 = int(0 + (dh/2))
    ymin3 = int(h - (dh/2))

t2 = "Centered"
box_1 = (xmin1,ymax1,xmax1,ymin1)
box_2 = (xmin2,ymax2,xmax2,ymin2)
box_3 = (xmin3,ymax3,xmax3,ymin3)

im1 = im.crop(box=box_1)
im2 = im.crop(box=box_2)
im3 = im.crop(box=box_3)

bt1 = ("1. Figure 1 ("+t1+" Trim)")
bt2 = ("2. Figure 2 ("+t2+" Trim)")
bt3 = ("3. Figure 3 ("+t3+" Trim)")

#plt.ion()

fig1 = plt.figure(1)
img1 = np.asarray(im1)
plt.axis('off')
fig1.tight_layout()
fig1.canvas.set_window_title(bt1)
plt.imshow(img1)

fig3 = plt.figure(2)
img3 = np.asarray(im3)
plt.axis('off')
fig3.tight_layout()
fig3.canvas.set_window_title(bt2)
plt.imshow(img3)

fig2 = plt.figure(3)
img2 = np.asarray(im2)
plt.axis('off')
fig2.tight_layout()
fig2.canvas.set_window_title(bt3)
plt.imshow(img2)

plt.show()

# GUI to ask user which image is desired
root = Tk()
root.title("Image save selection")
mainframe = ttk.Frame(root, padding="20 20 5 5")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
mode_select = IntVar()
Instructions = Label(mainframe, text = "Please select which image should be saved. \n")
Instructions.grid(column=2, row=0, sticky=(W, E), pady=5)
rb1 = ttk.Radiobutton(mainframe,text=bt1,variable=mode_select,value=1)
rb3 = ttk.Radiobutton(mainframe,text=bt2,variable=mode_select,value=3)
rb2 = ttk.Radiobutton(mainframe,text=bt3,variable=mode_select,value=2)
rb4 = ttk.Radiobutton(mainframe,text="4. Do not save any of them.",variable=mode_select,value=4)
#rb5 = ttk.Radiobutton(mainframe,text="5. Combine two MCNP output matrices (runs MUST be with same setup) ",variable=mode_select,value=5)
#rb6 = ttk.Radiobutton(mainframe,text="6. Re-bin a Response matrix",variable=mode_select,value=5)
#rb7 = ttk.Radiobutton(mainframe,text="7. Re-bin a pulse height or neutron energy spectrum ",variable=mode_select,value=6)
#rb8 = ttk.Radiobutton(mainframe,text="8. Smooth bins of a pulse height or neutron energy spectrum ",variable=mode_select,value=8)
rb1.grid(column=2, row=1, sticky=(W, E))
rb2.grid(column=2, row=3, sticky=(W, E))
rb3.grid(column=2, row=2, sticky=(W, E))
rb4.grid(column=2, row=4, sticky=(W, E))
#rb5.grid(column=2, row=5, sticky=(W, E))
#rb6.grid(column=2, row=6, sticky=(W, E))
#rb7.grid(column=2, row=7, sticky=(W, E))
#rb8.grid(column=2, row=8, sticky=(W, E))
select_button = ttk.Button(mainframe, text="Confirm Response", command = close_window)
select_button.grid(column=2, row=10, pady=20)
root.mainloop()
run_mode = mode_select.get()

print(run_mode)

if run_mode == 4:
    print("Save nothing.")
    sys.exit()
elif run_mode == 1:
    newfile = newfile_path_noex + "_n1.png"
    im1.save(newfile)
elif run_mode == 2:
    newfile = newfile_path_noex + "_n3.png"
    im2.save(newfile)
elif run_mode == 3:
    newfile = newfile_path_noex + "_n2.png"
    im3.save(newfile)
    
    
    
    
