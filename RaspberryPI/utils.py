# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions to display the pose detection results."""

import cv2
import numpy as np
from tflite_support.task import processor

_MARGIN = -35  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 2
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 255, 0)  # red

# Harsh wrote this method
def draw_text_bg(img, text, font=cv2.FONT_HERSHEY_PLAIN, pos = (0,0),
                 font_scale = 3, font_thickness = 2, text_color = (0,255,0),
                 text_color_bg=(0,0,0)):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, pos, (x+text_w, y+text_h), text_color_bg, -1)
    cv2.putText(img, text, (x, y+text_h+font_scale-1), font, font_scale, text_color, font_thickness)
    return img


def visualize(
    image: np.ndarray,
    detection_result: processor.DetectionResult,
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.

  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.

  Returns:
    Image with bounding boxes.
  """
  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

    # Draw label and score
    dummy_code = {'1':11, '2':12, '3':13, '4':14, '5':15, '6':16, '7':17, '8':18, '9':19, 'A':20, 'B':21, 'bullseye':10, 'C':22, 'D':23, 'Down':37, 'E':24, 'F':25, 'G':26, 'H':27, 'Left':39, 'Right':38, 'S':28, 'Stop':40, 'T':29, 'U':30, 'Up': 36,'V':31, 'W':32, 'X':33, 'Y':34, 'Z':35}
    category = detection.categories[0]
    category_name = category.category_name
    probability = round(category.score, 2)
    result_text = category_name + ' (' + str(probability) + ') id=' + str(dummy_code[category_name])
    text_location = (_MARGIN + bbox.origin_x,
                     _MARGIN + _ROW_SIZE + bbox.origin_y)
    '''cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS) # '''
    image = draw_text_bg(img = image, text = result_text, pos = text_location, font_scale = _FONT_SIZE)

  return image
