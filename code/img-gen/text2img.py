import torch
from diffusers import StableDiffusionPipeline

# model_id_or_path =  "runwayml/stable-diffusion-v1-5", 
model_id_or_path = "/project/models/arizwy.ckpt"
# model_id_or_path = "/project/models/bateman.ckpt"

pipe = StableDiffusionPipeline.from_single_file(
  model_id_or_path
  # torch_dtype=torch.float16
)
pipe = pipe.to("cuda")


# prompt = "a photo of an astronaut riding a horse on mars"
# prompt = "patrick bateman"
prompt = "a photo of arizwy"

image = pipe(prompt).images[0]

from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
image.save("tests/" + prompt + " " + now + ".png")


# https://arxiv.org/abs/2211.01777