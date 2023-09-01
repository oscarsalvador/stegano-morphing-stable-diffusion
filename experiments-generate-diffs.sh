MODEL_DIR="project/stable-diffusion/output/800"
SUBJECT="OscarSKS"
SUBJECT_TRAINING_IMG="project/training/IMG_20230821_140906.jpg"

mkdir experiments/sd-subject
for f in experiments/real-references/*; do 
  docker compose run --rm img-gen bash -c "python /img-gen/handler.py \
    --model_id_or_path /$MODEL_DIR \
    --prompt \"photo of $SUBJECT\" \
    --ref_img /$f \
    --out_dir /experiments/sd-subject/ \
    --generator img2img \
    --tries 10"
done

mkdir experiments/sd-actors2
docker compose run --rm img-gen bash -c "/experiments-code/experiment-2.sh"

