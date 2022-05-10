# HiFashion
HiFashion is a laptop application in which users can select clothes from the closet in the app to try out without the physical clothing. In the Home screen of the app, users can see themselves on the screen with their selected clothes resized and put onto their bodies, enabled by a body tracking ML solution from Mediapipe, and change clothes or their colors. In addition, users can also take a picture of themselves with the outfit and view it in the Saved Outfits gallery of the app. Making it easy for users to navigate, the app listens to voice commands by using the SpeechRecognition python library. Designed to be run conveniently, the app requires only the webcam and microphone from the laptop and a few packages or libraries, which could be installed easily with the given instructions.

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
- favs (directory)  
- icons (directory)  
- Body  

  A class that provides the body tracking service for the app.  
  
  - `track(self, img)`: Allows the app to pass in an image captured by the webcam and retrieve the on-screen coordinates of the shoulder and hip joints’ coordinates if a person is in the image. 
  - `in_sight(self, coor)`: Returns a coordinate only if the coordinate is within the screen boundary, otherwise `None`.
  - `draw(self, win)`: Draws out the skeleton of shoulders with a red line and the hip skeleton with a blue line, if they are visible on the screen.  

- ChangeColor  


- Closet  


- Constant  


- Fav  

  A class that corresponds to the Favorite (or Saved) Outifts Gallery in the app and responsible for updates occurring in the gallery.  
  
  - `to_fav(self)`: Called when the user decides to enter the saved outfits gallery. It will direct the user to the page where the user has left off last time (or page 1 if it is the first time the user enters here).
  - `update(self, text)`: Checks for keyboard commands and voice commands `text`, and update the statuses (which page the user is on, whether the user wants to exit the gallery) accordingly.
  - `compute_format(self)`: Called during initialization of the page to resize the image while preserving proportions for easier displaying and determine how many images per row.
  - `get_page(self, page)`: Goes to the given `page` in the gallery, if within the page boundaries, and update the screen with the page.
  - `saveOutfit(self, img)`: Saves the given `img` as a new saved outfit. Resize it and display in the gallery.

- FitClothes  


- HiFashion  


- Home  

  A class that corresponds to the Home page in the app, in which the user sees himself/herself on the screen, and responsible for any interactions happening in this page.  
  
  - `update(self, text)`: Checks for keyboard commands and voice commands `text`, and updates the statuses or executes the command accordingly.
  - `setNumClothes(self, num)`: Updates the instance variable `num_clothes` to `num` to ensure it knows the number of selected clothes at the momment.
  - `getSide(self)`: Tells whether the current clothes will fit the front of the user or the back of the user.  

- Speech  

  A class that provides the speech recognition service for the app.  
  
  - `get_text(self)`: Listens via the laptop's microphone and transcribe them into text with the use of the SpeechRecognition package. The text will be stored as an instance variable for the app to access.  




