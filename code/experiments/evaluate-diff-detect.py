import os
import argparse
import cv2
import csv
import ast

parser = argparse.ArgumentParser(description="Script to generate the CSV file dmimagedetection needs")
parser.add_argument("--csv_dir",  required=True,
  help="Dir with output of diff detect"
)

def main():
  args = vars(parser.parse_args())

  csvs = []
  for d in sorted(os.listdir(args["csv_dir"])):
    c = os.listdir(args["csv_dir"]  + d)[0]
    with open(args["csv_dir"] + d + "/" + c, 'r') as file:
      reader = csv.reader(file)
      csv_data = list(reader)[1:]
      csvs.append(csv_data)
  
  # print(csv_data )
  true_positives=0
  true_negatives=0
  false_positives=0
  false_negatives=0
  total=0
  real_count=0
  false_count=0

  for csv_data in csvs:
    for row in csv_data:
      total += 1

      print(row)
      # condicion verdadera, tiene difusion
      if not "real" in row[0]:
        # predictor dice que tiene difusion
        if float(row[3]) > 0:
          true_positives += 1
        else:
          false_negatives += 1
        real_count += 1

      # condicion falsa, no tiene difusion
      else:
        # predictor dice que no tiene
        if float(row[3]) < 0:
          true_negatives += 1
        else:
          false_positives += 1
        false_count += 1

      

  # for row in csv_data:
  #   pic_has_positive=False
  #   for row2 in csv_data:
  #     if row[0] == row2[0] and row2[3] == "True":
  #       pic_has_positive = True

  #   # condicion verdadera
  #   if "IMG" in row[0]:
  #     if pic_has_positive: 
  #       true_positives += 1
  #       tp_real += 1
  #       total_real += 1
  #     else: false_negatives += 1
      
  #   elif "img2img" in row[0]:
  #     if pic_has_positive: 
  #       true_positives += 1
  #       tp_diff += 1
  #       total_diff += 1
  #     else: false_negatives += 1

  #   # condicion negativa
  #   else:
  #     if pic_has_positive: false_positives += 1
  #     else: true_negatives += 1
    

  print("true_positives", true_positives, true_positives / total * 100)
  print("true_negatives", true_negatives, true_negatives / total * 100)
  print("false_positives", false_positives, false_positives / total * 100)
  print("false_negatives", false_negatives, false_negatives / total * 100)
  print("total", total)
  print("real count", real_count)
  print("false count", false_count)


if __name__ == "__main__":
  main()