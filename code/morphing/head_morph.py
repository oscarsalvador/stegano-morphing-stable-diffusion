import cv2
import numpy 


import faceops


def headmorph(src_path, dst_path, out_path, iterations):
  src_name = src_path.split("/")[-1]
  src_name = ".".join(src_name.split(".")[:-1])
  src_extension = "." + src_path.split(".")[-1]

  src = cv2.imread(dst_path)
  dst = cv2.imread(src_path)
  # safety resize
  h,w,c = src.shape
  dst = cv2.resize(dst, (w,h))

  # get coords of face in src
  x,y,h,w = faceops.find_face(src, False)

  # create mask to select morph zone
  # mask = numpy.zeros(src.shape[:2], dtype=numpy.uint8)
  # cv2.rectangle(mask, (x,y), (x+w, y+h), 255, -1)

  # src background
  # inv_mask = cv2.bitwise_not(mask)
  # cv2.bitwise_not(mask)
  # masked_src = cv2.bitwise_and(src, inv_mask)

  for i in range(1, iterations):
    # mask out everything except the face
    # mask = numpy.zeros(src.shape[:2], dtype=numpy.uint8)
    # cv2.rectangle(mask, (x, y), (x+w, y+h), 255,-1)

    # alpha is the weight of the first image, beta the second
    alpha_p = i/iterations 
    beta_p = 1 - alpha_p
    print(alpha_p, beta_p, alpha_p + beta_p)
    morphed = cv2.addWeighted(src, alpha_p, dst, beta_p, 0)

    # morphed head foreground
    # masked_morphed = cv2.bitwise_and(morphed, mask)
    # "region of interest" to be pasted on dst
    roi = morphed[y:y+h, x:x+w]
    result = dst.copy()
    result[y:y+h, x:x+w] = roi

    # result = cv2.add(masked_src, masked_morphed)

    cv2.imwrite(out_path + src_name + f"_head_{alpha_p:.2f}" + src_extension, result)

