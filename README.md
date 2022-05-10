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

Body is a class that basically provides body tracking service for the app. It has three functions: `track(self, img)`, `in_sight(self, coor)`, and `draw(self, win)`. The `track(self, img)` function allows the app to pass in an image captured by the webcam and retrieve the on-screen coordinates of the shoulder and hip joints’ coordinates if a person is in the image. The `in_sight(self, coor)` is a helper method that returns a coordinate only if the coordinate is within the screen boundary. The `draw(self, win)` function draws out the skeleton of shoulders with a red line and the hip skeleton with a blue line, if they are visible on the screen.  

- ChangeColor  
- Closet  
- Constant  
- Fav  
- FitClothes  
- HiFashion  
- Home  
- Speech  


