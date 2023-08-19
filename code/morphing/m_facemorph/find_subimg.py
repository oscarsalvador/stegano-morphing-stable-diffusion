import cv2

image = cv2.imread("destination_image-0.jpg")
# subimg = cv2.imread("frame018.png")
# subimg = cv2.imread("sub-0.jpg")
subimg = cv2.imread("resized_nose_img.jpg")

result = cv2.matchTemplate(image, subimg, cv2.TM_CCOEFF_NORMED)

print(cv2.minMaxLoc(result))
print("~~~~~~~~~~~~~~~~~~~")
print(result)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
print(max_loc)