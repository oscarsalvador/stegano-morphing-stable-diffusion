#!pip install deepface
from deepface import DeepFace
resp = DeepFace.verify("../caras-ejemplo/Richard_Stallman_at_LibrePlanet_2019.jpg", "../caras-ejemplo/Richard_M_Stallman_Swathanthra_2014_kerala.jpg", model_name = 'ArcFace')
print(resp)