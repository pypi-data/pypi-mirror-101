# Color Generator ![Python Powered](https://www.python.org/static/community_logos/python-powered-w-100x40.png "LOGO")
Handle color calculation in a pythonic way !  
**Feel free to contribute !!!**

## Installation
https://pypi.org/project/colorGenerator/  
Install from Pypi :
```bash
pip install colorGenerator
```
Import into your code and ready to go
```python
import colorGenerator as cG
```
## First step using colorGenerator
### 1 Converting RGB to HEX and HSL
```python
import colorGenerator as cG

# Print some color
red = cG.Color(rgb=(255, 0, 0))

# Representation of red in HEX
print(f"Representation of red in HEX : {red}")

# Representation of red in RGB
r, g, b = red.__repr__()
print(f"Representation of red in RGB : {(r, g, b)}")

# References
# http://en.wikipedia.org/wiki/HLS_color_space
# Representation of red in HSL
h, s, l = red.hsl()
print(f"Representation of red in HSL : {(h*360, s*100, l*100)}")

# Show the color in the Terminal
red.show()

cG.credits()
```
![Test1 result](test/capture/test1.png "Capture")

### 2 Finding complementary of a color and median of a palette
```python
import colorGenerator as cG

red = cG.Color(rgb=(255, 0, 0))
blue = cG.Color(rgb=(0, 255, 0))

# Find the complementary of red
c_red = red.complementary()
print("The complementary of red is : ", end="")
c_red.show()

# Find the median of red and blue
# We create a palette
palette = cG.Palette(colors=[red, blue])
med = palette.average_hsl()
print("The median of red and blue is : ", end="")
med.show()
```
![Test2 result](test/capture/test2.png "Capture")

### 3 Saving and Loading color and palette of colors
```python
import colorGenerator as cG

red = cG.Color(rgb=(255, 0, 0))
blue = cG.Color(rgb=(0, 255, 0))

# Save red into test3-red.json
red.save("test3-red.json")
# Loading saved color
load_red = cG.Color.load("test3-red.json")
print("The saved color is : ", end="")
load_red.show()

# We create a palette
palette = cG.Palette(colors=[red, blue])
# Save the palette test3-palette.json
palette.save("test3-palette.json")
# Loading saved palette
load_palette = cG.Palette.load("test3-palette.json")
print("The saved palette of red and blue is : ", end="")
load_palette.show()
```
![Test3 result](test/capture/test3.png "Capture")

### 4 Selecting automatically text color for an image
```python
import colorGenerator as cG
import cv2, requests
from PIL import Image, ImageDraw, ImageFont

# Let's Download the background image at
url = "https://raw.githubusercontent.com/tttienthinh/colorGenerator/main/test/test4-bg.jpg"
image = requests.get(url)
open("test4-bg.jpg", "wb").write(image.content)

# Pick two colors from the image
img = cv2.imread("test4-bg.jpg")
up_left_color = cG.Color(rgb=img[300, 480, ::-1])
down_right_color = cG.Color(rgb=img[1500, 2400, ::-1])

# This is the 2 picked colors from the image
up_left_color.show()
down_right_color.show()

# Creating the palette
palette = cG.Palette(colors=[
    up_left_color,
    down_right_color,
])

# Extrating the Average color
average_color = palette.average_rgb()
average_color.show()

# Creating the text color
text_color = average_color.complementary()
text_color.show()

# opening the image and writing text
img = Image.open("test4-bg.jpg")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("test4-font.ttf", 335)
draw.text((150, 320), text="colorGenerator", font=font, fill=text_color.__repr__())
img.save("test4-result.jpg")
```
![Test4 result](test/test4-result.jpg "Capture")

### 5 Picking color with Tkinter
```python
import colorGenerator as cG
from tkinter.colorchooser import askcolor

# Ask for a color
color = askcolor()
print(color[1])
r, g, b = color[0]

# Creating the color
new_color = cG.Color(rgb=(r, g, b))
new_color.show()
```
![Test5 result](test/capture/test5.png "Capture")
