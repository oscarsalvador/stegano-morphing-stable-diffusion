from PIL import Image
from diffusers import StableDiffusionControlNetPipeline, StableDiffusionImg2ImgPipeline, ControlNetModel, UniPCMultistepScheduler
import torch
from controlnet_aux import OpenposeDetector
from diffusers.utils import load_image

openpose = OpenposeDetector.from_pretrained('lllyasviel/ControlNet')

image = load_image("tests/photo_of_a_man.jpg")

image = openpose(image)

controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/sd-controlnet-openpose", torch_dtype=torch.float16
)

model_id_or_path = "/project/models/bateman"
    # "runwayml/stable-diffusion-v1-5", controlnet=controlnet, safety_checker=None, torch_dtype=torch.float16

# img2img_pipe = StableDiffusionImg2ImgPipeline.from_single_file(
#   model_id_or_path,
#   load_safety_checker=False,
#   device=0
# )
# # pipe = StableDiffusionControlNetPipeline.(
# #     model_id_or_path, controlnet=controlnet
# # )
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    model_id_or_path,
    controlnet=controlnet,
    torch_dtype=torch.float16,
    local_files_only=True
)

pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)

# Remove if you do not have xformers installed
# see https://huggingface.co/docs/diffusers/v0.13.0/en/optimization/xformers#installing-xformers
# for installation instructions
pipe.enable_xformers_memory_efficient_attention()

pipe.enable_model_cpu_offload()

image = pipe("photo of arizwy in color", image, num_inference_steps=20).images[0]

image.save('chef_pose_out.png')
