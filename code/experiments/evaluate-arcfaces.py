import os
import argparse
import cv2
import csv
import ast

parser = argparse.ArgumentParser(description="Script to generate the CSV file dmimagedetection needs")
parser.add_argument("--csv",  required=True,
  help="detailed_arcfaces.csv"
)

def main():
  args = vars(parser.parse_args())

  with open(args["csv"], 'r') as file:
    reader = csv.reader(file)
    csv_data = list(reader)[1:]
  
  # print(csv_data )
  true_positives=0
  tp_diff=0
  total_diff=0
  tp_real=0
  total_real=0
  true_negatives=0
  false_positives=0
  false_negatives=0
  total=0
  for row in csv_data:
    pic_has_positive=False
    for row2 in csv_data:
      if row[0] == row2[0] and row2[3] == "True":
        pic_has_positive = True

    # condicion verdadera
    if "IMG" in row[0]:
      if pic_has_positive: 
        true_positives += 1
        tp_real += 1
        total_real += 1
      else: false_negatives += 1
      
    elif "img2img" in row[0]:
      if pic_has_positive: 
        true_positives += 1
        tp_diff += 1
        total_diff += 1
      else: false_negatives += 1

    # condicion negativa
    else:
      if pic_has_positive: false_positives += 1
      else: true_negatives += 1
    
    total += 1

  print("true_positives", true_positives, true_positives / total * 100)
  print("true_negatives", true_negatives, true_negatives / total * 100)
  print("false_positives", false_positives, false_positives / total * 100)
  print("false_negatives", false_negatives, false_negatives / total * 100)
  print("total", total)
  print("true positives de reales", tp_real, total_real)      
  print("true positives de difusion", tp_diff, total_diff)


if __name__ == "__main__":
  main()