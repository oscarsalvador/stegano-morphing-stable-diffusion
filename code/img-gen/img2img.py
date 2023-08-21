import requests
import torch
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline


subject="bateman"
device = "cuda"
# model_id_or_path = "runwayml/stable-diffusion-v1-5"
# model_id_or_path = "/project/models/arizwy2.ckpt"
# model_id_or_path = "/project/models/arizwy-21.ckpt"
# model_id_or_path = "/project/models/skskmix.ckpt"
model_id_or_path = "/project/stable-diffusion/output/800/PatricBateman.ckpt"

# pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id_or_path, torch_dtype=torch.float16)
# pipe = StableDiffusionImg2ImgPipeline.from_ckpt(model_id_or_path)
pipe = StableDiffusionImg2ImgPipeline.from_single_file(
  model_id_or_path,
  load_safety_checker=False
)
pipe = pipe.to(device)

# url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"
# response = requests.get(url)
# init_image = Image.open(BytesIO(response.content)).convert("RGB")

init_image = Image.open("dst.jpg").convert("RGB")
# init_image = init_image.resize((768, 512))

prompt = "a photo of PatricBateman"# + subject + " man"

# guardar por timestamp, para pruebas de 1 en 1
images = pipe(prompt=prompt, image=init_image, strength=0.6, guidance_scale=7.5).images
from datetime import datetime
now = datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
images[0].save("tests/" + subject + "/" + now + ".png")

# generar rangos, para probar con weight
# max = 20
# for i in range(1, max):
#   decimal = i/max
#   images = pipe(prompt=prompt, image=init_image, strength=decimal, guidance_scale=7.5).images
#   images[0].save("tests/" + subject + "/" + f"{decimal:.2f}" + ".png")
