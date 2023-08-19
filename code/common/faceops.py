import cv2
import numpy 
from PIL import Image
import os



def find_face(img, highlight):
  # /usr/local/lib/python3.8/dist-packages/cv2/data/
  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
  # face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_righteye_2splits.xml')
  faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5)

  if highlight:
    for (x, y, w, h) in faces:
      cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
      cv2.putText(img, 'Face detected', (x+10, y+60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

  print("Detected faces", faces)

  biggest_detection = []
  detection_size = 0
  for face in faces:
    size = face[2] * face[3]
    if size > detection_size:
      detection_size = size
      biggest_detection = face

  print("Biggest area", biggest_detection)
    
  return biggest_detection



def zoom(img, face_rectangle, zoom_out, highlight):
  square_side = max(face_rectangle[2:3])
  zoom_pixels = square_side * (zoom_out/2)

  for coords in [0,1]:
    face_rectangle[coords] -= zoom_pixels
    if face_rectangle[coords] < 0: face_rectangle[coords] = 0

  for side in [2,3]:
    # by removing zoom_pixels from the start coords, the square is mooved to the top left, and now must be compensated
    face_rectangle[side] += zoom_pixels*2  

  print("Zoom out", zoom_out)
  print("Zoomed out", face_rectangle)
  if highlight:
    for (x, y, w, h) in [face_rectangle]:
      cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
      cv2.putText(img, 'Zoom', (x+10, y+60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

  return face_rectangle