import cv2
import numpy 
from PIL import Image
import os


import faceops


def find_subimage(image, subimg):
  result = cv2.matchTemplate(image, subimg, cv2.TM_CCOEFF_NORMED)

  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
  print("Find subimage", min_val, max_val, min_loc, max_loc)
  
  return max_loc


# def get_frame_coords(dst, last_frame):
#   # the last frame is the closest to the dst image

#   frame = cv2.imread(last_frame)
#   frame_face_rectangle = faceops.find_face(frame, True)
#   cv2.imwrite("here/frame.png", frame)
#   print("\nFace in facemorph start frame", frame_face_rectangle)

#   # to remove the edges of frame, which are transparent from the search, 
#   # zoom into the frame frame, getting the nose
#   (x, y, w, h) = faceops.zoom(
#     frame,
#     frame_face_rectangle.copy(),
#     -0.6,
#     False
#   )

#   print("Nose in facemorph frame", x, y)
#   nose_img = frame[y:y+h, x:x+w]

#   # facemorphed images have a different size from the originals, 
#   # to perform a subimage search, it has to be resized.
#   # To resize, the ratio has to be calculated

#   original_face_rectangle = faceops.find_face(dst, True)
#   cv2.imwrite("here/original.png", dst)
#   print("\nFace in original image", original_face_rectangle)

#   ratio = frame_face_rectangle / original_face_rectangle
#   print("Subimg/original ratio", ratio)
#   nose_img = cv2.resize(nose_img, (0,0), fx=ratio[2], fy=ratio[3])
  
#   nose_start_corner = find_subimage(dst, nose_img)

#   # nose in resized frame
#   x1 = x * ratio[2]
#   y1 = y * ratio[3]

#   # frame in original
#   x2 = int(nose_start_corner[0] - x1)
#   y2 = int(nose_start_corner[1] - y1)

#   print("Coords of frame in original", x2, y2)
#   return x2,y2,ratio


def get_frame_coords(dst_path, last_frame):
  # the last frame is the closest to the dst image
  frame = cv2.imread(last_frame)
  dst = cv2.imread(dst_path)

  eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_righteye_2splits.xml')
  frame_eyes = eyes_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
  dst_eyes = eyes_cascade.detectMultiScale(dst, scaleFactor=1.1, minNeighbors=5)

  # print(frame_eyes)
  # print(dst_eyes)
  # print()
  frame_eyedist = (frame_eyes[1][0] + frame_eyes[1][2]) - frame_eyes[0][0]
  dst_eyedist = (dst_eyes[1][0] + dst_eyes[1][2]) - dst_eyes[0][0]
  # print(frame_eyedist)
  # print(dst_eyedist)
  # print()
  ratio = frame_eyedist / dst_eyedist
  print(ratio)

  resized_frame = cv2.resize(frame, (0,0), fx=ratio, fy=ratio)

  xf,yf,wf,hf = frame_eyes[0]
  xd,yd,wd,hd = dst_eyes[0]

  print("frameeyes", xf, yf)
  print("dsteyes", xd, yd)

  # right eye in resized frame
  x1 = xf / ratio
  y1 = yf / ratio

  print("1", x1, y1)

  # resized frame in original
  x2 = int(xd - x1)
  y2 = int(yd - y1)

  print("2", x2, y2)
  # exit()
  # facemorphed images have a different size from the originals, 
  # to perform a subimage search, it has to be resized.
  # To resize, the ratio has to be calculated

  # original_face_rectangle = faceops.find_face(dst, True)
  # cv2.imwrite("here/original.png", dst)
  # print("\nFace in original image", original_face_rectangle)

  # ratio = frame_face_rectangle / original_face_rectangle
  # print("Subimg/original ratio", ratio)
  # nose_img = cv2.resize(nose_img, (0,0), fx=ratio[2], fy=ratio[3])
  
  # nose_start_corner = find_subimage(dst, nose_img)

  # nose in resized frame
  # x1 = x * ratio[2]
  # y1 = y * ratio[3]

  # frame in original
  # x2 = int(nose_start_corner[0] - x1)
  # y2 = int(nose_start_corner[1] - y1)

  print("Coords of frame in original", x2, y2)
  return x2,y2,ratio



def facemorph(src_path, dst_path, out_path, frames_dir, iterations, correction):

  frames = sorted(os.listdir(frames_dir))
  last_frame = frames_dir + frames[-1]

  x,y,ratio = get_frame_coords(dst_path, last_frame)

  # exit()
  src_name = src_path.split("/")[-1]
  src_name = ".".join(src_name.split(".")[:-1])
  src_extension = "." + src_path.split(".")[-1]

  # for every facemorph frame, create a new image pasting the frame on top of dst 
  original = Image.open(dst_path)
  for frame in frames:
    percentage = frames.index(frame)/len(frames)

    dst = original.copy()
    paste_image = Image.open(frames_dir + frame)
    paste_w = int(paste_image.size[0] / (ratio + correction))
    paste_h = int(paste_image.size[1] / (ratio + correction))

    resized_paste = paste_image.resize((paste_w, paste_h))

    print(x,y)
    print("Paste image", paste_w, paste_h)

    # mask = resized_paste.convert('RGBA')
    dst.paste(resized_paste, (x,y), resized_paste)

    dst.save(out_path + src_name + f"_face_{percentage:.2f}" + src_extension)


