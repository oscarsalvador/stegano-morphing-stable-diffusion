from PIL import Image

def fullmorph(src_path, dst_path, out_path, iterations):
  # separate source name from its dirs and extension
  src_name = src_path.split("/")[-1]
  src_name = ".".join(src_name.split(".")[:-1])

  src_extension = "." + src_path.split(".")[-1]
  dst_extension = "." + dst_path.split(".")[-1]
  
  if src_extension == "png":
    src = Image.open(src_path).convert("RGBA")
  else:
    src = Image.open(src_path)
  
  if dst_extension == "png":
    dst = Image.open(dst_path).convert("RGBA")
  else:
    dst = Image.open(dst_path)

  src = src.resize(dst.size, Image.BILINEAR)

  for i in range(1, iterations):
    alpha_p = i/iterations
    blended = Image.blend(src, dst, alpha=alpha_p)
    blended.save(out_path + src_name + f"_full_{alpha_p:.2f}" + src_extension)
