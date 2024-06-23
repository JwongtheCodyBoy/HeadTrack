<p align="center">
<img src="https://github.com/JwongtheCodyBoy/HeadTrack/assets/128951946/1468eb22-278e-4527-8964-6f42087710b8" width="701" height="527">
</p>

# Head Tracker
Basically a worst version of Michael Reeves's eye laser-er, I like my eyes so I can keep watching anime so I have it shoot my forehead instead

Made with Python and OpenCV libary to find and target a person's face. Using two Ardiuno servos, one strap on to another so a laser can be shined 

## To Use Head Tracker
Neeed to setup a python virtual enviroment for Open CV and also install OpenCV to work here is a video guide to do so
https://www.youtube.com/watch?v=fclTFQQvQFQ

Extra video in case short attention span to setup virtual enviorment
https://www.youtube.com/watch?v=GZbeL5AcTgw

**Four main Files**:
1. Python Script ("Face tracker" or "Face Tracker with no Ardiuno")
2. Arduino Sketch (in "sketch_may21a")
3. deploy.prototxt (Face detection for OpenCV)
4. res10_300x300_ssd_iter_140000_fp16.caffemodel (Data base used for OpenCV)

Python Scripts has two options
- First, Script where there is an Arduino connected to COMs. This script will open two windows displaying what computer sees and send JSON info to COMs for Arduino to do calculations with 
- Second, Script where there is NO Arduino present. This script will **ONLY** open two windows displaying what computer sees

Optional app.JS script

A simple backend API script that I made for python to write JSON data to the API instead of the COMs directly, but soon realized after completing the API that it was inefficent and should just write to COMs directly. 

**IMPORTANT NOTE**: This API script has the ablity to POST and GET, but the python script only POST to API, I did not complete the GET portion in the python script because I realized it was inefficent when writing it.

## General Information and Calibrattions
Code's uses Serial 9600 to communicate from Python to Ardiuno
Python does the finding and targeting 
Origin of Python (X, Y) is bottom left corner
Arduino does the calculations from X and Y positioning to servo angles

Head Tracker has a 2 Second Delay in updating position because if COMs are updated to fast Arduino will fail to read the data  

Calibrated distance is 1.8 feet from the camera can change in the **Arduino sketch**

**Python**:<br/>
Has an option to add offset to both X and Y positioning when sending JSON data (in case where the Arduino laser is very far from the origin)

**Arduino**:<br/>
Servo for X rotation (Yaw) default on Pin 9 <br/>
Servo for Y rotation (Pitch) default on Pin 11
