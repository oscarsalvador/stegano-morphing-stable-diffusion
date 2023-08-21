from diffusers import StableDiffusionInpaintPipeline
from diffusers import StableDiffusionImg2ImgPipeline
import torch
import PIL.Image
import cv2

# model_id_or_path = "/project/models/arizwy.ckpt"
model_id_or_path = "/project/models/bateman.ckpt"
# Load the pipeline
# pipe = StableDiffusionInpaintPipeline.from_pretrained(
#   # "stabilityai/stable-diffusion-2-inpainting",
#   local_checkpoint_path,
#   revision="fp16",
#   torch_dtype=torch.float16,
# ).to("cuda")

# no olvidar poner .to("cuda"), no asume por su cuenta que tenga que usar gpu y puede tardar x10-20 mas
im2img_pipe = StableDiffusionImg2ImgPipeline.from_single_file(
  model_id_or_path,
  load_safety_checker=False
).to("cuda")
inpaint_pipe = StableDiffusionInpaintPipeline(**im2img_pipe.components)


# Load the input image and mask
inp_img = PIL.Image.open("tests/photo_of_a_man.jpg")
mask = PIL.Image.open("masks/masktest2.png")

# Convert the input image to RGBA format
inner_image = inp_img.convert("RGBA")




subject = "bateman"
prompt = "" + subject

# Inpaint the masked region using Stable Diffusion
# out_image = inpaint_pipe(
#   inner_image,
#   mask,
#   prompt="yellow",
#   seed=torch.randint(0, 2 ** 32, ()),
#   guidance_scale=10.0,
#   step_count=100,
# )
out_image = inpaint_pipe(
  prompt,
  inner_image,
  mask,
)


# image = pipe(prompt=prompt, image=inp_img, mask_image=mask).images[0]

# Save the output image
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
# out_image.images[0].save("tests/" + prompt + "/" + now + ".png")
out_image.images[0].convert("RGB").save("tests/" + subject + "/inpainting/" + prompt + " " + now + ".png")

# counter = 30
# for i in out_image.images:
#   i.convert("RGB").save("noutput_image" + str(counter) + ".png")
#   counter += 1

# print(out_image)
# print(out_image.images)