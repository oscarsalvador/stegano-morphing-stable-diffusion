import os
import argparse
import cv2
import csv
import ast

import faceops

parser = argparse.ArgumentParser(description="Script to generate the CSV file dmimagedetection needs")
parser.add_argument("--dirs",  required=True,
  help="List of directories: eg ['dir1', 'dir2']"
)
parser.add_argument("--output",  required=True,
  help="Destination path for the resutling CSV"
)

def main():
  args = vars(parser.parse_args())
  dirs = ast.literal_eval(args["dirs"])

  diff_csv = [["src","cropsize","x1","y1","qf","typ","label"]]

  for d in dirs:
    if d[-1] != "/": d += "/"

    for i in sorted(os.listdir(d)):
      img = cv2.imread(d + i)
      x,y,w = (0,0,img.shape[1])

      # if no face is found, leave default values
      face = faceops.find_face(img, False)[0:3]
      if len(face) > 0:
        x,y,w = face[0:3]

      file_size = os.path.getsize(d+i)
      iw,ih = img.shape[0:2]
      compresion_guess = int(file_size / (iw*ih) * 100)
      if compresion_guess > 100: compresion_guess = 100
      compresion_guess = str(compresion_guess)

      type = d.split("/")[-2]

      label = "FALSE"
      if "real" in d: label = "TRUE"

      diff_csv.append([type + "/" + i,w,x,y,compresion_guess,type,label])

  with open(args["output"], "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(diff_csv)

  print(diff_csv)

if __name__ == "__main__":
  main()