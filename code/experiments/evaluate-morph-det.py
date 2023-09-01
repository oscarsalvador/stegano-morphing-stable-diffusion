import os
import argparse
import cv2
import csv
import ast

parser = argparse.ArgumentParser(description="Script to generate the CSV file SPL-MAD needs")
parser.add_argument("--csv_dir",  required=True,
  help="Dir with output of morph detect"
)

def main():
  args = vars(parser.parse_args())
  print(args)


  morph_rows = []
  for c in sorted(os.listdir(args["csv_dir"])):
    name = c.split("_result")[0]

    if ".csv" in c:
      print(args["csv_dir"] + c)
    # c = os.listdir(args["csv_dir"]  + d)[0]
      with open(args["csv_dir"] + c, 'r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)[1:]
      
      t = [t for t in sorted(os.listdir(args["csv_dir"])) if name + "_threshold.txt" in t][0]
      # print(t)

      with open(args["csv_dir"] + t, 'r') as file2:
        reader2 = csv.reader(file2)
        threshold_data = list(reader2)
      
      threshold = float(threshold_data[0][1].split("threshold is ")[-1])
      for row in csv_data:
        morph_rows.append([row[0], row[1], float(row[2]) > threshold])
      # print(csv_data)

  # print(morph_rows)  
  # print(csvs)
  
  true_positives=0
  true_negatives=0
  false_positives=0
  false_negatives=0
  total=0
  real_count=0
  false_count=0

  # print(csv_data)

  for row in morph_rows:
    total += 1

    print(row)
    # condicion verdadera, tiene morphing
    if row[1] == "attack":
      # predictor dice que tiene morphing
      if row[2]:
        true_positives += 1
      else:
        false_negatives += 1
      real_count += 1

    # condicion falsa, no tiene morphing
    else:
      # predictor dice que no tiene
      if row[1] == "bonafide":
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


if __name__ == "__main__":
  main()