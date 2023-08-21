FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update; apt-get upgrade -y
# ffmpeg libsm6 libxext6 necesarios para opencv
RUN apt-get install -y wget git ffmpeg libsm6 libxext6

RUN pip install -q -U --pre triton

# controlnet_aux and mediapipe are for controlnet pipelines
RUN pip install -q \
  accelerate \
  transformers \
  ftfy \
  bitsandbytes \ 
  gradio \
  natsort \ 
  safetensors \ 
  xformers \ 
  torchvision \ 
  python-dotenv \
  opencv-python \
  diffusers \
  omegaconf \
  controlnet_aux \
  mediapipe
