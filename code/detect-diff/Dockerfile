FROM tensorflow/tensorflow:latest-gpu

RUN apt-get update; apt-get upgrade -y
# ffmpeg libsm6 libxext6 necesarios para opencv
RUN apt-get install -y wget git ffmpeg libsm6 libxext6

RUN pip install -q -U --pre triton
RUN pip install -q \
  albumentations \
  boltons \
  cytoolz \
  Jinja2 \
  lmdb \
  matplotlib \
  numpy \
  pandas \
  Pillow \
  seaborn \
  sklearn \
  torch \
  torchvision \
  tqdm \ 
  # gdown \ breaks the installation
  python-dotenv 

RUN git clone https://github.com/grip-unina/dmimagedetection

# official pre-trained weights mentioned in the repo's readme. Gdrive isnt friendly to wget or curl
RUN pip install gdown
RUN gdown -O /dmimagedetection/weights.zip https://drive.google.com/uc?id=1sAoAuOGCWS4dAMBhDkRHgBf4SgBgvkVf&export=download; wait
RUN cd /dmimagedetection/; unzip weights.zip

