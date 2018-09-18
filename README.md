
# Convert_to_16_to_9_ratio.py


The purpose of this package is to convert background images of width W and height H pixels to a 16:9 aspect ratio. It seeks to produce several different altered versions of the input image, and the user can then save the one(s) that are desirable.  The three options provided for each case are shown below.

#### Cases for input image
W/H > 16/9  (x dimension must be trimmed):
    - Trim from left
    - Trim from right
    - Trim from both edges to keep image centered
W/H < 16/9  (y dimension must be trimmed):
    - Trim from top
    - Trim from bottom
    - Trim from both edges to keep image centered

The 16/9 value can be changed to some other aspect ratio by modifying the "desired_WoH_ratio" variable.
