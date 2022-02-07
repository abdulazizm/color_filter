import cv2
import numpy as np

img = cv2.imread('path/to/image.jpg') # give your image path
img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) # color space conversion - basic need for color filter
lower_red_limit = np.array([150,150,0]) # adjust values if required
upper_red_limit = np.array([180,255,255]) # adjust values if required

mask = cv2.inRange(img_hsv, lower_red_limit, upper_red_limit) # prepare mask - shows occurence of red color in the image

cv2.imshow(cv2.resize(img,(200,200)))
cv2.imshow(cv2.resize(mask,(200,200)))

# do application specific things - check if red color is in more than 10000 pixels
unique, counts = np.unique(mask, return_counts=True)
mask_dict = dict(zip(unique, counts))

if len(mask_dict) > 1 and mask_dict[255] > 10000: # fix this magic number (10000) as per need - this says "if mask_dict[255] is in 10000 pixels/dots in the image"
  print("Input image has red color")
else:
  print("Input image dont have red color")
