# Entornos virtuales
> python -m venv faces

> source faces/bin/activate

> source pruebas/bin/faces/activate

En VSCode 
1. ctrl+shift+p 
2. 'select interpreter' del venv

> deactivate


# Docker con aceleración gráfica
Requisitos
- Docker (Container Engine)
- `nvidia-docker-toolkit`

Usar la opción `--gpus all` al hacer `run` de un contenedor (ej. `docker run --rm -it --gpus all tensorflow/tensorflow:latest-gpu bash`), o incluir el siguiente código, a la altura de la imagen, en el servicio de docker-compose

```
deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Registro de imagenes de nvidia
https://catalog.ngc.nvidia.com/containers

# QEMU/KVM
No he podido configurar aceleración gráfica, parece que es con 'GPU Passthrough', y se necesita más de una tarjeta gráfica

