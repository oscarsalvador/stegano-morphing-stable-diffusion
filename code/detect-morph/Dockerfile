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

RUN git clone https://github.com/meilfang/SPL-MAD

# official pre-trained weights mentioned in the repo's readme. Gdrive isnt friendly to wget or curl with large files (security)
RUN pip install gdown
RUN gdown -O /SPL-MAD/casia_smdd.pth https://drive.google.com/uc?id=1kFLp1dWp_sBwC-l-RTVo-LRitKSYxbyv&export=download; wait