import cv2
import numpy as np

import serial.tools.list_ports
import serial
import json
import time

import threading

# import requests               ## API stuff

# Specify the paths to the files
prototxt_path = "./deploy.prototxt"
caffemodel_path = "./res10_300x300_ssd_iter_140000_fp16.caffemodel"

# URL for backend
# url = 'http://localhost:8080/data'

# Load the pre-trained deep learning face detection model
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # 0 means the default camera, change if you have multiple cameras

# Set the dimensions of the window
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 480

# Set Confidence level to draw
MIN_CONFI = 0.5

# Delay for Ardiuno and python connection
DELAY = 1

# Offset for the lazer pointer's position
xOffset = 0
yOffset = 0

# Slecting COM                                     Was using Serial COMs but that was dumb
ports = serial.tools.list_ports.comports()
portsList= []

print("Accessable COMs: ")
for one in ports:
    portsList.append(str(one))
    print(str(one))

if not portsList:
    print("No ports found, ending program")
    exit()

com = input("Select Com Port: ")

for i in range(len(portsList)):
    if portsList[i].startswith("COM"+str(com)):
        use = "COM"+str(com)
        print(f"using COM{str(com)}")
    else:
        print("No COMs found, Stoping program")
        exit()

# Configure the serial port
ser = serial.Serial(use, 9600) 
time.sleep(2)  # Wait for the connection to establish

thereIsFace = True


# Function to display the raw camera feed without delay
def display_raw_feed():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Raw Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

raw_feed_thread = threading.Thread(target=display_raw_feed)
raw_feed_thread.start()


# Loop to continuously get frames
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is captured successfully
    if not ret:
        print("Failed to capture image")
        break

    # Resize frame for better performance
    width = 480
    height = int(frame.shape[0] * (width / frame.shape[1]))
    frame_resized = cv2.resize(frame, (width, height))

    # Convert frame to blob for face detection model
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Set input to the face detection model and perform inference
    net.setInput(blob)
    detections = net.forward()


    middle_x = 0
    middle_y = 0
    corrected_y = 0
    # Loop over the detections
    for i in range(detections.shape[2]):                            ## remove loop for single target
        confidence = detections[0, 0, i, 2]  # Confidence score
        if confidence > MIN_CONFI:  # Filter out weak detections
            # Get the coordinates of the bounding box
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (startX, startY, endX, endY) = box.astype("int")

            # Draw the bounding box and confidence score on the frame
            text = "{:.2f}%".format(confidence * 100)
            y = startY - 10 if startY - 10 > 10 else startY + 10
            cv2.rectangle(frame_resized, (startX, startY), (endX, endY), (219, 148, 86), 2)                         ## Draw rectangle
            cv2.putText(frame_resized, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (210, 210, 210), 1)        ## Percentage

            middle_x = int((startX + endX) / 2)
            middle_y = int((startY + endY) / 2.25)
            cv2.circle(frame_resized, (middle_x, middle_y), 3, (100, 100, 225), -1)                                 ## Pointer at Head

            corrected_y = WINDOW_HEIGHT - middle_y
            # print(f'(x: {middle_x}, y: {middle_y})      offset y: {corrected_y}')

    # Resize the frame to fit the window size
    frame_resized = cv2.resize(frame_resized, (WINDOW_WIDTH, WINDOW_HEIGHT))



    ## Using API 
    # if middle_x:
    #     data = {
    #             "aimX": middle_x,
    #             "aimY": corrected_y  
    #         }
        
    #     print(f'(x: {data["aimX"]}, y: {middle_y})      offset y: {data["aimY"]}')
    #     # Send data to the API
    #     # json_data = json.dumps(data)
    #     response = requests.post(url, json=data)

    #     # Print the response from the server
    #     print(response.text)
    # else:
    #     data = {
    #             "aimX": 0,
    #             "aimY": 0
    #         }
        
    #     print(f'(x: {data["aimX"]}, y: {middle_y})      offset y: {data["aimY"]}')
    #     response = requests.post(url, json=data)
    #     print(response.text)

    ## Using COMS
    if middle_x:
        thereIsFace = True
        data = {
                "aimX": middle_x,
                "aimY": corrected_y + yOffset   
            }
        print(f'(x: {data["aimX"]}, y: {data["aimY"]})      before correction y: {middle_y}')
        # Convert the JSON object to a string         
        json_data = json.dumps(data)
        # Send the JSON string to the Arduino
        ser.write(json_data.encode('utf-8'))
    elif not middle_x and thereIsFace:
        thereIsFace = False
        data = {
                "aimX": 0,
                "aimY": 0  
            }
        json_data = json.dumps(data)
        ser.write(json_data.encode('utf-8'))
        print(f'(x: {data["aimX"]}, y: {data["aimY"]})      no face found')

    # Display the resulting frame
    cv2.imshow('Face Tracking', frame_resized)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if ser.in_waiting > 0:
        response = ser.read_until().decode('utf-8').strip()
        print(response)
    time.sleep(DELAY)

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
# Close Serial port
ser.close()
