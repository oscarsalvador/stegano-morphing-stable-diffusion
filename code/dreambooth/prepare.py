import os
from pathlib import Path

import argparse
from dotenv import load_dotenv

import json


import random
import time

load_dotenv()
env_hf_token = os.getenv("HUGGINGFACE_TOKEN")


parser = argparse.ArgumentParser(description="Script to execute dreambooth without jupyter notebook")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--subject", help="Name of the person")
group.add_argument("--concepts_list", help="If training multiple concepts, use a json")

parser.add_argument("--model_name", default="runwayml/stable-diffusion-v1-5",
  help="Name in huggingface of the model to use"
)
parser.add_argument("--subject_class", default="person",
  help="Subject's class"
)
parser.add_argument("--instance_data_dir", default="/project/stable-diffusion/data/",
  help="Local dir with the training images of the subject"
)
parser.add_argument("--output_dir", default="/project/stable-diffusion/output",
  help="Local dir where new model will be saved"
)
parser.add_argument("--class_data_dir", default="/project/stable-diffusion/data/",
  help="Local dir for images of the subject's class"
)
# boolean
parser.add_argument("-p", "--preprocess_images", action='store_true', 
  help="Toggle wether to create new images in a new /prep folder for each subject"
)
parser.add_argument("-z", "--zoom_percentage", default=0.3, type=float,
  help="Percentage of the image to zoom out, zero to one, higher meaning the face is further away"
)
parser.add_argument("-s", "--image_side_len", default=512, 
  help="Desired final length for the square images to be prepared"
)
parser.add_argument("--highlight", action="store_true", default=False, 
  help="Highlight detection rectangles"
)

CONTRAST_COLORS = [
  (0, 0, 255, 255),
  (0, 255, 0, 255),
  (255, 0, 0, 255),
  (255, 255, 0, 255),
  (255, 0, 255, 255),
  (0, 255, 255, 255)
]
args = vars(parser.parse_args())

if args["preprocess_images"]:
  import cv2
  from PIL import Image
  import rembg
  import io
  import numpy 
      


def write_concepts_json(args, concepts_list_path):
  instance_data_directories = []

  # if single subject through args
  if args["concepts_list"] == None:
    instance_dir = single_concept_json(args, concepts_list_path)
    instance_data_directories.append(instance_dir)

  # if using a concepts_list.json
  else: 
    if os.path.exists(args["concepts_list"]):
      # concepts_list_path = args["concepts_list"]
      with open(args["concepts_list"], "r") as f:
        new_json = json.load(f)
        # if images are to be preprocessed, they images to train will be in a /prep subdir
        if args["preprocess_images"]: 
          for concept in new_json:
            concept["instance_data_dir"] += "/prep"
        
        with open(concepts_list_path, "w") as newfile:
          json.dump(new_json, newfile, indent=4)
          
    else:
      print("concepts_list.json not found")
      exit()


def single_concept_json(args, concepts_list_path):
  instance_data_dir = args["instance_data_dir"]
  class_data_dir = args["class_data_dir"]

  if args["instance_data_dir"] == "/project/stable-diffusion/data/":
    instance_data_dir += args["subject"]
  # if images are to be preprocessed, they images to train will be in a /prep subdir
  if args["preprocess_images"]: 
    instance_data_dir += "/prep"
  if args["class_data_dir"] == "/project/stable-diffusion/data/":
    class_data_dir += args["subject_class"]

  concepts_list = [
    {
      "instance_prompt":   "photo of " + args["subject"] +  " " + args["subject_class"],
      "class_prompt":      "photo of a " + args["subject_class"],
      "instance_data_dir": instance_data_dir,
      "class_data_dir":    class_data_dir
    }
  ]

  directory = os.path.dirname(concepts_list_path)
  os.makedirs(directory, exist_ok=True)

  with open(concepts_list_path, "w") as f:
    json.dump(concepts_list, f, indent=4)

  return instance_data_dir




def replace_background(img):
  transparent = rembg.remove(img)

  color = CONTRAST_COLORS[random.randint(0,len(CONTRAST_COLORS) -1)]
  background = Image.new("RGBA", transparent.size, color)
  background.paste(transparent, (0,0), transparent)

  image_array = numpy.array(background.convert("RGBA"))

  output = cv2.cvtColor(image_array, cv2.COLOR_RGBA2BGR)

  return output
    



def find_face(img, highlight):
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




def crop_and_write(img, coords, side_len, dir):
  (x, y, w, h) = coords
  cropped_img = img[y:y+h, x:x+w]

  resized_img = cv2.resize(cropped_img, (side_len, side_len), interpolation=cv2.INTER_LINEAR)

  new_path = dir + "/prep/" + str(time.time()) + ".jpg"

  cv2.imwrite(new_path, resized_img)







def main():
  # create ~/.huggingface/token and model output dir
  hf_path  = str(Path.home()) + "/.cache/huggingface"
  os.makedirs(hf_path, exist_ok=True)  

  with open(hf_path + "/token", "w") as f:
    f.write(str(env_hf_token))

  os.makedirs(args["output_dir"], exist_ok=True)
  

  # # find or create concepts_list.json
  # concepts_list_path = "stable-diffusion/concepts_list.json"
  tmp = args["instance_data_dir"]
  if tmp[-1] != "/": tmp += "/"
  concepts_list_path = tmp.split("/")[-3] + "/concepts_list.json"
  write_concepts_json(args, concepts_list_path)
  write_concepts_json(args, concepts_list_path)

  # create instance_data_dir for every concept 
  image_dirs = []
  with open(concepts_list_path, "r") as f:
    for concept in json.load(f):
      # print(concept)
      os.makedirs(concept["instance_data_dir"], exist_ok=True)
      dir = concept["instance_data_dir"].split("/prep")[0]
      image_dirs.append(dir)

  # print(image_dirs)


  # preprocess images if so selected
  if not args["preprocess_images"]:
    print("Copy the appropriate trainig images to:")
    for d in image_dirs:
      print("  " + d) 
  else:

    for d in image_dirs:
      for i in os.listdir(d):
        full_path = os.path.join(d, i)
        if not os.path.isdir(full_path):
          attempts = 5
          print("\n\n",full_path)
          
          # sometimes faces are not found, or errors can occur
          while(attempts > 0):
            try:
              img = Image.open(full_path)
              clean_background = replace_background(img)

              face_rectangle = find_face(clean_background, args["highlight"])

              new_rectangle = zoom_out(
                clean_background, 
                face_rectangle, 
                args["zoom_percentage"], 
                args["highlight"]
              )

              crop_and_write(
                clean_background, 
                new_rectangle, 
                args["image_side_len"], 
                d
              )

              attempts = 0
            except:
              attempts -= 1





if __name__ == "__main__":
  main()