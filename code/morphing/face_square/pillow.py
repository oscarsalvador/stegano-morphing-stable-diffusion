
from PIL import Image
import cv2
import numpy 
from PIL import Image
import os


def find_face(img, highlight):
  # /usr/local/lib/python3.8/dist-packages/cv2/data/
  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
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



# Open the images
# img1 = Image.open("source_image-0.jpg").convert("RGBA")
# img2 = Image.open("destination_image-0.jpg").convert("RGBA")
src = cv2.imread("source_image-0.jpg")
dest = cv2.imread("destination_image-0.jpg")

x,y,h,w = find_face(src, False)
# print(face)
mask = numpy.zeros(src.shape[:2], dtype=numpy.uint8)
cv2.rectangle(mask, (x, y), (x+w, y+h), 255,-1)

morphed = cv2.addWeighted(src, 0.5, dest, 0.5, 0)
# masked = cv2.bitwise_and(morphed, morphed, mask=mask)
# result = cv2.add(dest, masked)

# region de interes
roi = morphed[y:y+h, x:x+w]
dest[y:y+h, x:x+w] = roi

cv2.imwrite("result.jpg", dest)

# print(find_face(src,False))

# for i in range(1,20):
#   alpha_p=i/20
#   print(alpha_p)

#   # Blend the images
#   blended = Image.blend(img1, img2, alpha=alpha_p)

#   # Display the result
#   blended.save("pillow_test_" + f"{alpha_p:.2f}" + ".png")