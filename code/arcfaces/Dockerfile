FROM tensorflow/tensorflow:latest-gpu


# COPY cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN apt update; apt upgrade -y
RUN apt-get install -y wget 
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin -O /etc/apt/preferences.d/cuda-repository-pin-600


# RUN pip install -qq git+https://github.com/ShivamShrirao/diffusers
RUN apt install -y cuda
RUN python3 -m pip install --upgrade pip
RUN pip install -q -U --pre triton
RUN pip install -q python-dotenv testresources
RUN pip install -q deepface --ignore-installed

#RUN apt-get install -y libgl1-mesa-glx
#face_recognition