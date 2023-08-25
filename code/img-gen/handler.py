from PIL import Image
from datetime import datetime
from io import BytesIO
import argparse

import torch
from diffusers import StableDiffusionImg2ImgPipeline, StableDiffusionPipeline, StableDiffusionInpaintPipeline, StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
from diffusers.utils import load_image
from controlnet_aux import OpenposeDetector


parser = argparse.ArgumentParser(description="Script to images through different stable diffusion pipelines")

parser.add_argument("--model_id_or_path", required=True,
  help="Huggingface model id or local path (ckpt or dreambooth output folder)"
)
parser.add_argument("--prompt", required=True,
  help="Text to guide the generated image"
)
parser.add_argument("--ref_img", required=True,
  help="Reference image for img2img, inpaint, and controlnet"
)
parser.add_argument("--out_dir", required=True,
  help="Directory into which to save the generated images"
)
parser.add_argument("--generator", required=True,
  choices=["text2img", "img2img", "inpaint", "controlnet"],
  help="Way to use stable diffusion"
)
parser.add_argument("--tries", default=1, type=int,
  help="How many images to generate for the given parameters"
)


def text2img(model_id_or_path, prompt, output_img_path):
  # pipe = StableDiffusionPipeline.from_single_file(
  pipe = StableDiffusionPipeline.from_pretrained(
    model_id_or_path,
    load_safety_checker=False
  )
  pipe = pipe.to("cuda")

  image = pipe(prompt).images[0]
  image.save(output_img_path)



def img2img(model_id_or_path, input_img_path, prompt, output_img_path):
  # pipe = StableDiffusionImg2ImgPipeline.from_single_file(
  pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id_or_path,
    load_safety_checker=False
  )
  pipe = pipe.to("cuda")

  init_image = Image.open(input_img_path).convert("RGB")
  # init_image = init_image.resize((768, 512))

  image = pipe(prompt=prompt, image=init_image, strength=0.6, guidance_scale=7.5).images[0]
  image.save(output_img_path)



def inpaint(model_id_or_path, input_img_path, mask_path, prompt, output_img_path):
  inpaint_pipe = StableDiffusionInpaintPipeline.from_pretrained(
    model_id_or_path,
    load_safety_checker=False,
    torch_dtype=torch.float16
  )
  inpaint_pipe = inpaint_pipe.to("cuda")

  # init_image = load_image(input_img_path)
  # mask = load_image(mask_path)
  init_image = Image.open(input_img_path).convert("RGBA")
  w,h = init_image.size
  mask = Image.open(mask_path).convert("RGBA")

  image = inpaint_pipe(
    prompt,
    init_image,
    mask,
  ).images[0]
  image = image.resize((w,h))
  image.save(output_img_path)



def controlnet(model_id_or_path, input_img_path, prompt, output_img_path):
  openpose = OpenposeDetector.from_pretrained("lllyasviel/ControlNet")
  # openpose = OpenposeDetector.from_pretrained("lllyasviel/openpose_face")

  init_image = load_image(input_img_path)
  openpose_image = openpose(init_image)
  openpose_image.save("/project/img-gen/openpose.png")
  
  controlnet = ControlNetModel.from_pretrained(
      "lllyasviel/sd-controlnet-openpose"
  )

  controlnet_pipe = StableDiffusionControlNetPipeline.from_pretrained(
    model_id_or_path,
    controlnet=controlnet,
    local_files_only=True
  )
  controlnet_pipe.scheduler = UniPCMultistepScheduler.from_config(controlnet_pipe.scheduler.config)
  controlnet_pipe.enable_xformers_memory_efficient_attention()
  controlnet_pipe.enable_model_cpu_offload()

  controlnet_image = controlnet_pipe(
    prompt, 
    openpose_image, 
    num_inference_steps=20
  ).images[0]
  controlnet_image.save(output_img_path)

# def controlnet(model_id_or_path, input_img_path, prompt, output_img_path):


def main():
  args = vars(parser.parse_args())

  print(args)

  for i in range(0,args["tries"]):
    # save by timestamp, for one by one testing
    now = datetime.now().strftime("_%Y-%m-%d_%H:%M:%S.%f_")
    output_img_path = args["out_dir"] + args["generator"] +  now + ".png"
    
    if args["generator"] == "text2img":
      text2img(args["model_id_or_path"], args["prompt"], output_img_path)

    if args["generator"] == "img2img":
      img2img(args["model_id_or_path"], args["ref_img"], args["prompt"], output_img_path)
    
    if args["generator"] == "inpaint":
      inpaint(args["model_id_or_path"], args["ref_img"], "/project/masktest2.png", args["prompt"], output_img_path)

    if args["generator"] == "controlnet":
      controlnet(args["model_id_or_path"], args["ref_img"], args["prompt"], output_img_path)


if __name__ == "__main__":
  main()
