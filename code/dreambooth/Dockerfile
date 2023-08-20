FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update; apt-get upgrade -y
# ffmpeg libsm6 libxext6 necesarios para opencv
RUN apt-get install -y wget git ffmpeg libsm6 libxext6

RUN pip install -qq git+https://github.com/ShivamShrirao/diffusers
RUN pip install -q -U --pre triton
RUN pip install -q \
  accelerate \
  transformers \
  ftfy \
  bitsandbytes==0.35.0 \
  gradio \
  natsort \ 
  safetensors \ 
  xformers \ 
  torchvision \ 
  python-dotenv \
  opencv-python \
  rembg

#face_recognition