import cv2
import numpy 


import faceops


def headmorph(src_path, dst_path, out_path, iterations):

  src = cv2.imread(src_path)
  dst = cv2.imread(dst_path)

  # get coords of face in src
  x,y,h,w = faceops.find_face(src, "haarcascade_frontalface_alt2.xml", False)

  src_name = src_path.split("/")[-1]
  src_name = ".".join(src_name.split(".")[:-1])
  src_extension = "." + src_path.split(".")[-1]

  for i in range(1, iterations):
    # mask out everything except the face
    # mask = numpy.zeros(src.shape[:2], dtype=numpy.uint8)
    # cv2.rectangle(mask, (x, y), (x+w, y+h), 255,-1)

    alpha_p = i/iterations
    beta_p = 1 - alpha_p
    morphed = cv2.addWeighted(src, alpha_p, dst, beta_p, 0)
    
    # "region of interest" to be pasted on dst
    roi = morphed[y:y+h, x:x+w]
    dst[y:y+h, x:x+w] = roi

    cv2.imwrite(out_path + src_name + f"_head_{alpha_p:.2f}" + src_extension, dst)

