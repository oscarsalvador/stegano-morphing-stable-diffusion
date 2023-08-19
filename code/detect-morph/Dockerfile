FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update; apt-get upgrade -y
# ffmpeg libsm6 libxext6 necesarios para opencv
RUN apt-get install -y wget git ffmpeg libsm6 libxext6

RUN pip install -q -U --pre triton
RUN pip install -q \
  opencv-python \
  matplotlib \
  numpy \
  scipy \
  tqdm \
  pandas \
  albumentations \
  torchvision \
  python-dotenv 