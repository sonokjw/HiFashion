# HiFashion
HiFashion is a laptop application in which users can select clothes from the closet in the app to try out without the physical clothing. In the Home screen of the app, users can see themselves on the screen with their selected clothes resized and put onto their bodies, enabled by a body tracking ML solution from Mediapipe, and change clothes or their colors. In addition, users can also take a picture of themselves with the outfit and view it in the Saved Outfits gallery of the app. Making it easy for users to navigate, the app listens to voice commands by using the SpeechRecognition python library. Designed to be run conveniently, the app requires only the webcam and microphone from the laptop and a few packages or libraries, which could be installed easily with the given instructions.

Specific instructions on how to use the system is at Section 2 System Description link: https://docs.google.com/document/d/1YRuiOz7zrQK0OXn5wvelsQ9iFtwe3P-uX6dIABZgEQI/edit?usp=sharing

## Table of Content
#### Section I: Setup and Running Instruction
#### Section II: File Descriptions  
.  
.  
### I. Instruction to run:

In the current stage, the app only supports running on **MacOS** and **not with M1 Chip**.  
Make sure to have Python 3.6+.  

Below is the step by step guide:

##### Activate a Python virtual environment:

```
$ python3 -m venv my_env && source my_env/bin/activate
```

##### Install requirements:

```
(my_env)$ pip3 install -r requirements.txt
```

##### After that, you could run the program:

```
(my_env)$ python3 HiFashion.py
```

##### When exit, deactivate the environment:

```
$ deactivate
```

### II. File Descriptions  

- clothes (directory)  

  A directory for all the clothes in the closet. Images will be in `.png` format, and the naming convention for clothes' front images will be consecutive integers starting from 0. For back images, which are optional, it will be in the format of integer + 'b' with integer the same as the clothes' front images. It also has a .csv file which is used for storing the three offsets for each clothes image.
  
- favs (directory) 
 
  A directory for all saved pictures that are displayed in Saved Outfits Gallery page.
  
- icons (directory)  

  A directory for all pictures for different buttons.

- Body  

  A class that provides the body tracking service for the app.  
  
  - `track(self, img)`: Allows the app to pass in an image captured by the webcam and retrieve the on-screen coordinates of the shoulder and hip joints’ coordinates if a person is in the image. 
  - `in_sight(self, coor)`: Returns a coordinate only if the coordinate is within the screen boundary, otherwise `None`.
  - `draw(self, win)`: Draws out the skeleton of shoulders with a red line and the hip skeleton with a blue line, if they are visible on the screen.  

- ChangeColor  

  Functions that support color changing for clothings: `lumiChromi(pixel)`, `change_color(cloth, new_color)`. The `lumiChromi(pixel)` returns a luminance and chrominance map of a pixel of an image. The `change_color(cloth, new_color)` changes the color scheme to the new color by replacing the chrominance map of the clothing image according to the new color.  
  
- Closet  

  A class that corresponds to the Closet in the app and responsible for updates occurring while the user is in Closet.  
  
  - `to_closet(self)`: Called when the user decides to enter the Closet. It will direct the user to the page where the user has left off last time (or page 1 if it is the first time the user enters here).
  - `update(self, text, event)`: Checks for keyboard commands, voice commands `text`, and mouse hover/click `event` for clothes selection, after which it should update the instance variables and executes the command (page changing, clothes selection, exit Closet, etc.) accordingly.
  - `get_page(self, page)`: Goes to the given `page` in Closet, if within the page boundaries, and update the screen with the page.
  - `organizeClothes(self, clothes)`: Takes in a dictionary of clothes_ind mapped to images of the clothes `[front, back (optional)]`, and create a list of Hanger instances, one for each clothes. Images are rescaled such that they all fit into a bounding box with pre-set dimensions for the purpose of better displaying.
  - `rescale(self, img)`: Rescales the given `img` such that it fits into a bounding box of dimensions set by us.
  - `getSelected(self)`: Returns the list of selected Hangers (clothes).
  - `getNumSelected(self)`: Returns number of selected clothes.

- Constant  

  Stores constants, classes, and helper functions needed for different pages of the app.  

  - constants: mainly the RGB color values, coordinates, and integers. 
  - processing of photos and margin data located in clothes(directory)
  - Button (class): Creates functionality of buttons wiht functions such as `on_click, show`, `change_mode`. 
  - Hanger (class): Stores all necessary information for a single clothes including its front and back views. It is also responsible for closet interactions of clothes through `on_click` and `show functions`.  
  - `load_clothes()`: Loads clothes from the clothes directory returns a dictionary mapping the clothes number to a list of images `[front, back]` in which `back` is optional.

- Fav  

  A class that corresponds to the Favorite (or Saved) Outifts Gallery in the app and responsible for updates occurring in the gallery.  
  
  - `to_fav(self)`: Called when the user decides to enter the saved outfits gallery. It will direct the user to the page where the user has left off last time (or page 1 if it is the first time the user enters here).
  - `update(self, text)`: Checks for keyboard commands and voice commands `text`, and update the statuses (which page the user is on, whether the user wants to exit the gallery) accordingly.
  - `compute_format(self)`: Called during initialization of the page to resize the image while preserving proportions for easier displaying and determine how many images per row.
  - `get_page(self, page)`: Goes to the given `page` in the gallery, if within the page boundaries, and update the screen with the page.
  - `saveOutfit(self, img)`: Saves the given `img` as a new saved outfit. Resize it and display in the gallery.

- FitClothes  

  Functions that support clothes fitting: `calc_dist(loc1, loc2)`, `fitClothes(cloth, location, cloth_type, margin)`, `fitCoords (location, cloth_type, margin_w, margin_h)`. The function `fitClothes(cloth, location, cloth_type, margin)` fits the clothes on the body according to where the fitting point should be located on the user's body. The function `fitCoords (location, cloth_type, margin_w, margin_h)` aligns body fitting point with the left most shoulder point of the clothing.  
  
- HiFashion  

  The main integrator file that supports the application's user interaction mechanism and navigation through different pages of the app.
- Home  

  A class that corresponds to the Home page in the app, in which the user sees himself/herself on the screen, and responsible for any interactions happening in this page.  
  
  - `update(self, text)`: Checks for keyboard commands and voice commands `text`, and updates the statuses or executes the command accordingly.
  - `setNumClothes(self, num)`: Updates the instance variable `num_clothes` to `num` to ensure it knows the number of selected clothes at the momment.
  - `getSide(self)`: Tells whether the current clothes will fit the front of the user or the back of the user.  

- Speech  

  A class that provides the speech recognition service for the app.  
  
  - `get_text(self)`: Listens via the laptop's microphone and transcribe them into text with the use of the SpeechRecognition package. The text will be stored as an instance variable for the app to access.  




