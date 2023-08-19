import os
import argparse
import cv2
import csv

import faceops


parser = argparse.ArgumentParser(description="Script to generate the csv dmimagedetection consumes")
parser.add_argument("--src",  required=True,
  help="Source image with the subject"
)
parser.add_argument("--morphs",  required=True,
  help="Directory where all the morphing dirs are"
)


def main():
  args = vars(parser.parse_args())

  img = cv2.imread(args["src"])

  x,y,w = faceops.find_face(img, False)[0:3]

  iw,ih = img.shape[0:2]
  file_size = os.path.getsize(args["src"])
  compresion_guess = str(int(file_size / (iw*ih) * 100))

  morphs = args["morphs"]
  if morphs[-1] != "/": morphs += "/"
  morphs_dirs = sorted(os.listdir(morphs))

  m_csv = [["src","cropsize","x1","y1","qf","typ","label"]]
  for d in morphs_dirs:
    d = morphs+d
    print(d)
    if not os.path.isdir(d): continue

    type = d.split("/")[-1]

    img_list = sorted(os.listdir(d))
    for i in img_list:
      m_csv.append([type + "/" + i,w,x,y,compresion_guess,type,"FALSE"])


  with open("detect-diff.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(m_csv)




if __name__ == "__main__":
  main()
