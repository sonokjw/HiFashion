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
- ChangeColor  
- Closet  
- Constant  
- Fav  
- FitClothes  
- HiFashion  
- Home  
- Speech  


