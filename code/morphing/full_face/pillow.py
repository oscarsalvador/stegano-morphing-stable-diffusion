
from PIL import Image

# Open the images
img1 = Image.open("source_image.png").convert("RGBA")
img2 = Image.open("destination_image.png").convert("RGBA")

# Ensure both images are the same size
img1 = img1.resize(img2.size, Image.BILINEAR)

for i in range(1,20):
  alpha_p=i/20
  print(alpha_p)

  # Blend the images
  blended = Image.blend(img1, img2, alpha=alpha_p)

  # Display the result
  blended.save("pillow_test_" + f"{alpha_p:.2f}" + ".png")