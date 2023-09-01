import os
import argparse
import cv2
import csv
import ast
import shutil

parser = argparse.ArgumentParser(description="Script to generate the CSV file dmimagedetection needs")
parser.add_argument("--morph_csv_dir",  required=True,
  help="Dir with output of morph detect"
)
parser.add_argument("--diff_csv_dir",  required=True,
  help="Dir with output of diff detect"
)
parser.add_argument("--output",  required=True,
  help="Destination path for the resutling CSV"
)
parser.add_argument("--filter", required=True,
  help="Only measure a particular type of morphing"
)
parser.add_argument("--copy", required=True,
  help="Copy the images that trick both to a new dir"
)

def main():
  args = vars(parser.parse_args())
  print(args)

  diff_csvs = []
  for d in sorted(os.listdir(args["diff_csv_dir"])):
    c = os.listdir(args["diff_csv_dir"]  + d)[0]
    with open(args["diff_csv_dir"] + d + "/" + c, 'r') as file:
      reader = csv.reader(file)
      csv_data = list(reader)[1:]
      diff_csvs.append(csv_data)


  morph_rows = []
  for c in sorted(os.listdir(args["morph_csv_dir"])):
    name = c.split("_result")[0]

    if ".csv" in c:
      print(args["morph_csv_dir"] + c)
    # c = os.listdir(args["morph_csv_dir"]  + d)[0]
      with open(args["morph_csv_dir"] + c, 'r') as file:
        reader = csv.reader(file)
        csv_data = list(reader)[1:]
      
      t = [t for t in sorted(os.listdir(args["morph_csv_dir"])) if name + "_threshold.txt" in t][0]
      # print(t)

      with open(args["morph_csv_dir"] + t, 'r') as file2:
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

  tricked_both = []
  for morph_row in morph_rows:
    for diff_csv in diff_csvs:
      for diff_row in diff_csv:
        if diff_row[0] in morph_row[0]:
          if args["filter"] != "none":
            if not args["filter"] in diff_row[0]:
              continue

          total +=1


          # condicion verdadera: tiene difusión y morphing 
          if (not "0.00" in diff_row[0] and not "1.00" in diff_row[0]) and morph_row[1] == "attack":
            # se detecta difusion o morphing
            if (float(diff_row[3]) > 0) or morph_row[2]:
              true_positives += 1
            else:
              false_negatives += 1
              tricked_both.append([diff_row[0]])
          # no tiene difusion, morphing, o ninguno
          else:
            # se detecta difusion o morphing
            if (float(diff_row[3]) > 0) or morph_row[2]:
              false_positives += 1
            else:
              true_negatives += 1


    # morph_total += 1

    # print(row)
    # # condicion verdadera, tiene morphing
    # if row[1] == "attack":
    #   # predictor dice que tiene morphing
    #   if row[2]:
    #     morph_true_positives += 1
    #   else:
    #     morph_false_negatives += 1
    #   real_count += 1

    # # condicion falsa, no tiene morphing
    # else:
    #   # predictor dice que no tiene
    #   if row[1] == "bonafide":
    #     morph_true_negatives += 1
    #   else:
    #     morph_false_positives += 1
    #   false_count += 1

  with open(args["output"] + "filter_" + args["filter"] + "_combined-detect.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(tricked_both)

  if args["copy"] == "true":
    for i in tricked_both:
      # print(i[0])
      try:
        shutil.copy("/experiments/experiment-3/" + i[0], "/experiments/experiment-5-arcfaces")
      except:
        print("No encontrada", i)
        continue

  print("true_positives", true_positives, true_positives / total * 100)
  print("true_negatives", true_negatives, true_negatives / total * 100)
  print("false_positives", false_positives, false_positives / total * 100)
  print("false_negatives", false_negatives, false_negatives / total * 100)
  print("total", total)







  
  





if __name__ == "__main__":
  main()