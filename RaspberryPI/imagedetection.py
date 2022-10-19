import argparse
import sys
import time

import cv2

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import tensorflow_lite_support
import utils


def captureImage():
    cap = cv2.VideoCapture(0) # video capture source camera (Here webcam of laptop) 
    ret,frame = cap.read(0) # return a single frame in variable `frame`
    #cv2.imshow('img1',frame) #display the captured image
    # cv2.imwrite('image.jpg',frame)
    
    # Rotate the image by 180 degrees
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    
    cv2.destroyAllWindows()
    return frame

def runModel(image, model ="model80epochs_new.tflite"):
    # Visualization parameters
    dummy_code = {'1':11, '2':12, '3':13, '4':14, '5':15, '6':16, '7':17, '8':18, '9':19, 'A':20, 'B':21, 'bullseye':10, 'C':22, 'D':23, 'Down':37, 'E':24, 'F':25, 'G':26, 'H':27, 'Left':39, 'Right':38, 'S':28, 'Stop':40, 'T':29, 'U':30, 'Up': 36,'V':31, 'W':32, 'X':33, 'Y':34, 'Z':35}
    row_size = 20  # pixels
    left_margin = 24  # pixels
    text_color = (0, 0, 255)  # red
    font_size = 1
    font_thickness = 1
    fps_avg_frame_count = 10

     # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=model, use_coral=False, num_threads=4)
    detection_options = processor.DetectionOptions(
        max_results=3, score_threshold=0.35)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)

    # Run object detection estimation using the model.
    detection_result = detector.detect(input_tensor)
    
    # Dealing with multiple objects detected
    best_name = detection_result.detections[0].categories[0].category_name
    best_confidence = detection_result.detections[0].categories[0].score
    best_area = detection_result.detections[0].bounding_box.width * detection_result.detections[0].bounding_box.height
    best_dummy_code = str(dummy_code[best_name])
    best_index = 0
    # print(type(detection_result))
    i = 1
    while(i < len(detection_result.detections)):
        name = detection_result.detections[i].categories[0].category_name
        confidence = detection_result.detections[i].categories[0].score
        area = detection_result.detections[i].bounding_box.width * detection_result.detections[i].bounding_box.height
        if(confidence > 0.6):
            if(area > best_area) and (area - best_area > best_area//5):  # If area atleast 20% larger than previous best then replace
                best_name = name
                best_confidence = confidence
                best_area = area
                best_index = i
                best_dummy_code = str(dummy_code[best_name])
            elif(confidence > best_confidence):  # Otherwise take best confidence
                best_name = name
                best_confidence = confidence
                best_area = area
                best_index = i
                best_dummy_code = str(dummy_code[best_name])
        i += 1
    
    # Make new detection result
    new_detection_result = tensorflow_lite_support.python.task.processor.proto.detections_pb2.DetectionResult([detection_result.detections[best_index]])
    #new_detection_result.detections = [detection_result.detections[best_index]]
    
    # Draw keypoints and edges on input image
    image = utils.visualize(image, new_detection_result)
    
    #print("-------------Detected: ", detection_result.detections[0].categories[0].category_name)  # Harsh Added this
    #print("----------------Score: ", detection_result.detections[0].categories[0].score)  # Harsh Added this
    return best_name, best_confidence, image

# Script to test this Program (Comment Later when calling in production)
#img = captureImage()
#name, confidence, image = runModel(img)
#cv2.imwrite('./images/image.jpg', image)
#print("--------Result: ", name, " (", confidence, ")")

