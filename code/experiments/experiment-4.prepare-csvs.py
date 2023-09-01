import os
import argparse
import cv2
import csv
import ast

import faceops

parser = argparse.ArgumentParser(description="Script to generate the CSV file dmimagedetection needs")
parser.add_argument("--dir",  required=True,
  help="Parent directory to the ones with the morphed images"
)
parser.add_argument("--output",  required=True,
  help="Destination path for the resutling CSV"
)
parser.add_argument("--handpicked",  required=True,
  help="Handmade CSV with the references and difusion images"
)
parser.add_argument("--filter",  required=True,
  help="Which of 'head', 'full' or 'face' to use"
)


def main():
  args = vars(parser.parse_args())
  print(args)

  with open(args["handpicked"], 'r') as file:
    reader = csv.reader(file)
    csv_data = list(reader)
    
  directories = sorted(os.listdir(args["dir"]))
  directories = [d for d in directories if args["filter"] in d]
  directories = [d for d in directories if os.path.isdir(args["dir"] + d)]

  
  for d in directories:
    d_path = args["dir"] + d

    dir_reference_img = ""

    for row in csv_data:
      if len(row) < 3: continue # skip trailing newlines
      if row[0] == "Identifier": continue # skip first line
      
      if row[0] in d:
        dir_reference_img = row[1]
        if dir_reference_img[0] == " ": dir_reference_img = dir_reference_img[1:]

    morph_csv = []
    print(d, dir_reference_img)
    for i in sorted(os.listdir(d_path)):
      # print(i)
      morph_csv.append([d_path + "/" + i, "attack"])

    # write two csvs per dir, each with 50 so as to not run out of memory
    first_half = [["img_path","labels"]]
    first_half += morph_csv[0:50]
    first_half.append(["/experiments/" + dir_reference_img, "bonafide"])

    # print(first_half)

    second_half = [["img_path","labels"]]
    second_half += morph_csv[50:]
    second_half.append(["/experiments/" + dir_reference_img, "bonafide"])

    # print()
    # print(second_half)

    with open(args["output"] + d + "0-50.csv", "w", newline="") as file1:
      writer1 = csv.writer(file1)
      writer1.writerows(first_half)
    
    with open(args["output"] + d + "50-100.csv", "w", newline="") as file2:
      writer2 = csv.writer(file2)
      writer2.writerows(second_half)
    

if __name__ == "__main__":
  main()