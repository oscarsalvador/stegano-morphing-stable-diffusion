import os
import argparse
import cv2
import csv

import faceops


parser = argparse.ArgumentParser(description="Script to generate the csv dmimagedetection consumes")
parser.add_argument("--dst",  required=True,
  help="Destination image, target of morphing"
)
parser.add_argument("--morphs",  required=True,
  help="Directory where all the morphing dirs are"
)
parser.add_argument("--batch_size",  required=True,
  help="For the morphing detector to not run out of memory, the list is split. The last list will have the last batch and the remainder, that is, up to batch_size*2 -1"
)


def main():
  args = vars(parser.parse_args())

  img = cv2.imread(args["dst"])

  x,y,w = faceops.find_face(img, False)[0:3]

  iw,ih = img.shape[0:2]
  file_size = os.path.getsize(args["dst"])
  compresion_guess = str(int(file_size / (iw*ih) * 100))

  morphs = args["morphs"]
  parent_dir = os.path.abspath(morphs)

  if morphs[-1] != "/": morphs += "/"
  morphs_dirs = sorted(os.listdir(morphs))
  diff_csv = [["src","cropsize","x1","y1","qf","typ","label"]]
  morph_csv = []

  for d in morphs_dirs:
    d = morphs+d
    if not os.path.isdir(d): continue
    print(d)

    type = d.split("/")[-1]

    img_list = sorted(os.listdir(d))
    for i in img_list:
      diff_csv.append([type + "/" + i,w,x,y,compresion_guess,type,"FALSE"])
      morph_csv.append([parent_dir + "/" + type + "/" + i, "attack"])

  with open(morphs + "/detect-diff.csv", "w", newline="") as file1:
    writer1 = csv.writer(file1)
    writer1.writerows(diff_csv)

  # morph detector loads all images of the csv at the same time, 
  # needs to be split up to not run out of memory
  # i don't want too few images in the last batch, so I join the 
  # last two together

  batch_size = int(args["batch_size"])
  length = len(morph_csv)
  remainder = length % batch_size
  batches = int(length / batch_size)

  sublists = [morph_csv[i:i+batch_size] for i in range(0, length, batch_size)]
  sub_length = len(sublists)
  for i in range(0, (sub_length -1)):
    # print(i, sub_length)
    sublist =  [["img_path","labels"]]
    if i == sub_length -2:
      # print(sublists[i][0][0], sublists[i+1][-1][0])
      sublist += sublists[i] + sublists[i+1]
      # print(sublist[0][0], sublist[-1][0])
    else:
      sublist += sublists[i]
      # print(sublists[i][0][0], sublists[i][-1][0])

    # print(sublist[0][0],sublist[1][0], sublist[-1][0])

    sublist.append([os.path.abspath(args["dst"]), "bonafide"])
    with open(morphs + "/detect-morph_" + str(i +1) + "_of_" + str(sub_length -1) + ".csv", "w", newline="") as file2:
      writer2 = csv.writer(file2)
      writer2.writerows(sublist)  



if __name__ == "__main__":
  main()