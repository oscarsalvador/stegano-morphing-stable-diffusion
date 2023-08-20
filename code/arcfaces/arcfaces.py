import argparse
import json
import os
import ast
import csv

from deepface import DeepFace

parser = argparse.ArgumentParser(description="Script to recognice faces in a set of images")
parser.add_argument("--people",  required=True,
  help="List of lists string with k-v pairs where k is the person and v the image path. Eg --people \"[['source', '$SRC_IMG'], ['diffusion', '$DST_IMG]]\""
)
parser.add_argument("--images_dir",  required=True,
  help="Directory with the images to be scanned"
)
parser.add_argument("--out_dir",  required=True,
  help="Directory into which to write the output csvs"
)

# models = [
#   "VGG-Face", 
#   "Facenet", 
#   "Facenet512", 
#   "OpenFace", 
#   "DeepFace", 
#   "DeepID", 
#   "ArcFace", 
#   "Dlib", 
#   "SFace",
# ]

# verification = DeepFace.verify("destination_image-0.jpg", "source_image-0.jpg", model_name = models[1])
# # recognition = DeepFace.find(img_path = "img.jpg", db_path = “C:/facial_db", model_name = models[1])
# print(verification)

# # dfs = DeepFace.find(img_path = "img1.jpg",
# #       db_path = "C:/workspace/my_db", 
# #       model_name = models[1]
# # )

def main():
  args = vars(parser.parse_args())

  images_dir = args["images_dir"]
  if images_dir[-1] != "/": images_dir += "/"
  out_dir = args["out_dir"]
  if out_dir[-1] != "/": out_dir += "/"
  
  people = ast.literal_eval(args["people"])

  best_match_csv = [["Scanned image", "Detected person", "Verified", "Distance", "Threshold"]]
  detailed_csv = [["Scanned image", "Detected person", "Verified", "Distance", "Threshold"]]
  for i in sorted(os.listdir(images_dir)):
    best_distance = 1000
    best_result = None
    best_person = None

    for p in people:
      for photo in p[1]:
        result = DeepFace.verify(
          img1_path = images_dir + i, 
          img2_path = photo, 
          model_name="ArcFace"
        )

        if result["distance"] < best_distance:
        # if result["verified"] == True:
          best_result = result
          best_distance = result["distance"]
          best_person = p

        print(images_dir + i, p[0], result)
        # /project/morphing/head/src_head_0.01.jpg diffusion {'verified': True, 'distance': 0.02642844230042607, 'threshold': 0.68, 'model': 'ArcFace', 'detector_backend': 'opencv', 'similarity_metric': 'cosine', 'facial_areas': {'img1': {'x': 166, 'y': 148, 'w': 342, 'h': 342}, 'img2': {'x': 167, 'y': 148, 'w': 342, 'h': 342}}, 'time': 0.36}
        detailed_csv.append([images_dir + i, p[0], photo, result["verified"], result["distance"], result["threshold"]])
    best_match_csv.append([images_dir + i, p[0], best_result["verified"], best_distance, best_result["threshold"]])

  # print(detailed_csv)
  # print("\n\n\n\n")
  # print(best_match_csv)

  with open(out_dir + "detailed_arcfaces.csv", "w", newline="") as file1:
    writer1 = csv.writer(file1)
    writer1.writerows(detailed_csv)

  with open(out_dir + "best_match_arcfaces.csv", "w", newline="") as file2:
    writer2 = csv.writer(file2)
    writer2.writerows(best_match_csv)


if __name__ == "__main__":
  main()