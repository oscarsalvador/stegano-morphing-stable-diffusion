import cv2
import numpy 
from PIL import Image
import os

# def extract_center():
def find_subimage(image, subimg):
  # image = cv2.imread("destination_image-0.jpg")
  # subimg = cv2.imread("frame018.png")
  # subimg = cv2.imread("sub-0.jpg")
  # subimg = cv2.imread("resized_nose_img.jpg")

  result = cv2.matchTemplate(image, subimg, cv2.TM_CCOEFF_NORMED)

  # print(cv2.minMaxLoc(result))
  # print("~~~~~~~~~~~~~~~~~~~")
  print(result)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
  return max_loc

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

def zoom_out(img, face_rectangle, zoom_out, highlight):
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
      cv2.putText(img, 'Zoom out', (x+10, y+60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

  return face_rectangle

# subimg = cv2.imread("sub-0.jpg")
subimg = cv2.imread("frame018.png")

subimg_face_rectangle = find_face(subimg, False)
print("Face in facemorphed", subimg_face_rectangle)

(x, y, w, h) = zoom_out(
  subimg,
  subimg_face_rectangle,
  -0.6,
  False
)
print("Nose in facemorphed", x, y)

nose_img = subimg[y:y+h, x:x+w]
# cv2.rectangle(subimg, (x, y), (x+w, y+h), (0,0,255), 3)
# cv2.imwrite("new14.jpg", subimg)

# la imagen de face morpher tiene un tamaño distintos a la original, por lo que hay que ajustarlo para poder hacer una busqueda de subimagen que tenga sentido
image = cv2.imread("destination_image-0.jpg")
original_face_rectangle = find_face(image, False)
# print(original_face_rectangle)
# lado horizontal, normalmente cuadrados, pero puede valer
ratio = subimg_face_rectangle / original_face_rectangle
print("Subimg/original ratio", ratio)

nose_img = cv2.resize(nose_img, (0,0), fx=ratio[3], fy=ratio[3])
# cv2.imwrite("resized_nose_img.jpg", nose_img)

start_corner = find_subimage(image, nose_img)
print("Resized nose_img top left corner in original", start_corner)
# print(start_corner)


resized_facemorph = cv2.resize(subimg, (0,0), fx=ratio[3], fy=ratio[3])

# nose in resized facemorph
x1 = x * ratio[3]
y1 = y * ratio[3]

# facemorph in original
x2 = start_corner[0] - x1
y2 = start_corner[1] - y1

print("facemorph in original", x2, y2)







# pegar facemorph sobre la original

# Load the main image and the image to paste
main_image = Image.open('destination_image-0.jpg')

folder = "facemorpher/"
frames = os.listdir(folder)
for frame in frames:
  paste_image = Image.open(folder + frame)
  paste_x = int(paste_image.size[0] * ratio[3])
  paste_y = int(paste_image.size[1] * ratio[3])

  resized_paste = paste_image.resize((paste_x, paste_y))

  print("Paste image", paste_x, paste_y)


# Define the coordinates to paste the image
# x, y = 100, 200

# Create a mask from the paste image
  mask = resized_paste.convert('RGBA')

# Paste the image onto the main image at the specified coordinates with the mask
  main_image.paste(resized_paste, (int(x2), int(y2)), mask)

# Save the modified image
  main_image.save('full_facemorphed/' + frame)


# height, width, channels = resized_facemorph.shape
# print("height ,w ", height, width)
# roi = image[y2:y2+height, x2:x2+width]
# img2gray = cv2.cvtColor(resized_facemorph,cv2.COLOR_BGR2GRAY)
# ret, mask = cv2.threshold(img2gray, 10, 255, cv2.THRESH_BINARY)
# mask_inv = cv2.bitwise_not(mask)
# image_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
# image_fg = cv2.bitwise_and(resized_facemorph,resized_facemorph,mask = mask)
# dst = cv2.add(image_bg,image_fg)
# image[y2:y2+height, x2:x2+width] = dst


# cv2.imwrite("pastetest.jpg", image)
# falta encojer subimg, restar a su tama