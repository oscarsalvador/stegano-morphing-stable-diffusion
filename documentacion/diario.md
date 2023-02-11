# 2023 w6
- Toma de contacto, llamada con Eduardo

- [ ] Leer y Buscar en google scholar los papeles que citen a *Real or fake? spoofing state-of-the-art face synthesis detection systems*
  - Leer todos, segun numero de citas y cercanía a mi objetivo, en más detalle
    - [ ] *Deepfakes and beyond: A survey of face manipulation and fake detection*
      | Paper | Implementacion | Instalacion |
      | - | - | - |
      | *Detecting and Simulating Artifacts in GAN Fake Images (Extended Version)* | https://github.com/ColumbiaDVMM/AutoGAN | Probando |
      | *A Simple Baseline for Spotting AI-Synthesized Fake Faces*/*Face X-ray for More General Face Forgery Detection* | No encontrada | |
      | *DeepFake Detection by Analyzing Convolutional Traces* (L. Guarnera) | No encontrada | |
      | *Detecting GAN Generated Fake Images Using Co-Occurrence Matrices* | No encontrada | |
      | *Attributing Fake Images to GANs: Learning and Analyzing GAN Fingerprints* | No encontrada | |
      | *Incremental learning for the detection and classification of GAN-generated images* | Encontrado https://github.com/Coral79/CDDB, pero es un set y de otro papel, solo que para este | |
      | *Detecting CNN-Generated Facial Images in Real-World Scenarios* | No encontrada | |

- Elegir, por ahora al menos, dos "malos", detectores de caras y spoofing, que intentar engañar, como objetivo
  - En *Deepfakes and beyond* hablan de once, ver los dos que mas prometan y que consiga correr
    - AutoGAN (promete)
    - 

- Pruebas fallidas con redes generativas antagónicas. Problemas porque son antiguos y las versiones de python que usan tienen conflictos que no consigo resolver
  - https://github.com/DarkGeekMS/Retratista
  - https://github.com/SummitKwan/transparent_latent_gan
  - https://github.com/dmonn/dcgan-oreilly
  - https://github.com/zllrunning/face-parsing.PyTorch
  - https://github.com/velpegor/Face_customizing

- Prueba exitosa con Stable Diffusion usando un docker-compose distinto
  - https://github.com/AbdBarho/stable-diffusion-webui-docker
    - Automatic1111 esta roto, no funcionan los servicios (del compose) `auto` y `auto-cpu`
    - Invoke funciona, incluido img2img, pero solo con GPU
  - Pruebas con la funcionalidad imagen a imagen, usando distintas configuraciones para buscar la generacion de caras más realistas


# 2023 w5
- Despliegue exitoso de Stable Diffusion en Docker con aceleración gráfica
  - https://github.com/pieroit/stable-diffusion-jupyterlab-docker
  - https://code.mendhak.com/run-stable-diffusion-on-ubuntu/#get-the-model-file

  - Modelos en: https://replicate.com/stability-ai/stable-diffusion/versions

- Stable Diffusion fallidos:
  - https://github.com/fboulnois/stable-diffusion-docker
    - Depurado, y funcionando, pero no he conseguido buena calidad de imagenes
  - https://github.com/Husseinfo/stable-diffusion-docker

- Pruebas de código exitosas con Eigenfaces y ArcFace (solo he podido con la librería `deepfaces`). Guardadas en `reconocimiento/eigenfaces` y `reconocimiento/arcfaces`
  - https://towardsdatascience.com/eigenfaces-face-classification-in-python-7b8d2af3d3ea
  - https://scipy-lectures.org/packages/scikit-learn/auto_examples/plot_eigenfaces.html

  - https://learnopencv.com/face-recognition-with-arcface/
  - https://github.com/chenggongliang/arcface
  - https://pypi.org/project/arcface/

- Pruebas fallidas con FaceNet
  - https://pypi.org/project/facenet/
  - https://www.kaggle.com/code/yhuan95/face-recognition-with-facenet

# 2023 w4 
- Pruebas con entornos virtuales, QEMU y nvidia-docker-toolkit
  - https://catalog.ngc.nvidia.com/containers

